import base64
import os
import queue
import subprocess
import threading
import time
import sys

from mcp.server.fastmcp import Context, FastMCP

# --- CONFIGURATION ---
TIMEOUT_SECONDS = 300  # Kill session after 5 minutes of inactivity
WARM_POOL_SIZE = 1  # Keep 1 container ready to go


class DockerSandbox:
    def __init__(self):
        print(
            "Container starting... (this may take 10-20s for the first run)",
            file=sys.stderr,
        )
        self.last_used = time.time()
        env = os.environ.copy()
        env["DOCKER_HOST"] = "unix:///var/run/docker.sock"

        self.process = subprocess.Popen(
            [
                "docker",
                "run",
                "--rm",
                "-i",
                "--memory=2024m",
                "--cpus=1.0",
                "-v",
                f"{os.getcwd()}/data:/data:rw",
                "ghcr.io/astral-sh/uv:python3.12-bookworm-slim",
                "uv",
                "run",
                "--with",
                "pandas",
                "--with",
                "matplotlib",
                "-q",
                "python",
                "-iqu",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0,
            env=env,
        )
        self._wait_for_ready()

        # Setup matplotlib non-interactive backend immediately
        self.execute(
            "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt"
        )

    def _wait_for_ready(self):
        try:
            self.process.stdin.write("print('READY')\n")
            self.process.stdin.flush()
            while True:
                line = self.process.stdout.readline()
                if "READY" in line:
                    print("Container ready!", file=sys.stderr)
                    break
                if not line:
                    raise RuntimeError("Container died during startup.")
        except Exception as e:
            print(f"Startup failed: {e}", file=sys.stderr)
            raise

    def execute(self, code):
        self.last_used = time.time()  # Update activity timestamp
        sentinel = "###__END__###"
        print(f"DEBUG: Execute called with code:\n{code}", file=sys.stderr)
        b64_code = base64.b64encode(code.encode("utf-8")).decode("utf-8")
        wrapper = f"exec(__import__('base64').b64decode('{b64_code}'))"

        try:
            self.process.stdin.write(wrapper + "\n")
            self.process.stdin.write(f"print('{sentinel}')\n")
            self.process.stdin.flush()
        except BrokenPipeError:
            return "Error: Container died."

        output_lines = []
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            if sentinel in line:
                break
            output_lines.append(line.rstrip())

        return "\n".join(output_lines)

    def close(self):
        """Force kills the docker process."""
        try:
            self.process.terminate()
            self.process.wait(timeout=2)
        except Exception:
            self.process.kill()


# --- SESSION MANAGER ---
class SandboxManager:
    def __init__(self):
        self.active_sessions = {}  # { session_id: DockerSandbox }
        self.warm_pool = queue.Queue(maxsize=WARM_POOL_SIZE)
        self.lock = threading.Lock()

        # Start background threads
        threading.Thread(target=self._monitor_timeouts, daemon=True).start()
        threading.Thread(target=self._fill_pool, daemon=True).start()

    def get_sandbox(self, session_id):
        with self.lock:
            # 1. Return existing session if active
            if session_id in self.active_sessions:
                return self.active_sessions[session_id]

            # 2. Assign from warm pool (Instant!)
            if not self.warm_pool.empty():
                print(f"[{session_id}] Assigned WARM sandbox.", file=sys.stderr)
                sandbox = self.warm_pool.get()
                self.active_sessions[session_id] = sandbox
                # Trigger refill in background
                threading.Thread(target=self._fill_pool, daemon=True).start()
                return sandbox

        # 3. Fallback: Create new (Slow) if pool was empty
        print(
            f"[{session_id}] Warm pool empty. Creating new (wait required)...",
            file=sys.stderr,
        )
        sandbox = DockerSandbox()
        with self.lock:
            self.active_sessions[session_id] = sandbox
        return sandbox

    def _fill_pool(self):
        """Maintains the warm pool size."""
        # Check size without lock first to avoid blocking
        if self.warm_pool.qsize() >= WARM_POOL_SIZE:
            return

        print("Refilling warm pool...", file=sys.stderr)
        try:
            # Create sandbox (slow operation) outside lock
            sb = DockerSandbox()
            self.warm_pool.put(sb)
            print("Warm pool replenished.", file=sys.stderr)
        except Exception as e:
            print(f"Failed to fill pool: {e}", file=sys.stderr)

    def _monitor_timeouts(self):
        """Background thread to kill idle sessions."""
        while True:
            time.sleep(10)
            now = time.time()
            to_remove = []

            with self.lock:
                for sid, sb in self.active_sessions.items():
                    if now - sb.last_used > TIMEOUT_SECONDS:
                        to_remove.append(sid)

            for sid in to_remove:
                print(f"[{sid}] Session timed out. Killing container.", file=sys.stderr)
                sb = self.active_sessions.pop(sid)
                sb.close()


# --- MCP SERVER ---
manager = SandboxManager()
mcp = FastMCP("DockerSandbox")


@mcp.tool()
def execute_python(code: str, ctx: Context) -> str:
    """
    Executes Python code in a persistent Docker sandbox with pandas installed.
    State (variables, imports) persists between calls.
    """
    session_id = str(id(ctx.session))
    sandbox = manager.get_sandbox(session_id)
    return sandbox.execute(code)


@mcp.tool()
def inspect_variables(ctx: Context) -> str:
    """
    Returns a string representation of all local variables in the current session.
    Useful for debugging what data is currently available in memory.
    """
    session_id = str(id(ctx.session))
    sandbox = manager.get_sandbox(session_id)
    # We filter out internal stuff usually, but let's just dump locals()
    # except standard things if we want to be fancy.
    # For now, just print locals() but convert to string carefully.
    code = "import pprint; pprint.pprint({k:v for k,v in locals().items() if not k.startswith('_') and k not in ['pprint', 'base64', 'os', 'sys']})"
    return sandbox.execute(code)


if __name__ == "__main__":
    # Run as an SSE server (standalone)
    print(
        f"Server starting. Timeout: {TIMEOUT_SECONDS}s. Warm Pool: {WARM_POOL_SIZE}",
        file=sys.stderr,
    )
    mcp.run(transport="sse")
