# import base64
# import os
# import subprocess
#
# from mcp.server.fastmcp import FastMCP
#
#
# class DockerSandbox:
#     def __init__(self):
#         env = os.environ.copy()
#         env["DOCKER_API_VERSION"] = "1.44"
#         self.process = subprocess.Popen(
#             [
#                 "docker",
#                 "run",
#                 "--rm",
#                 "-i",
#                 "--memory=512m",
#                 "--cpus=1.0",
#                 "-v",
#                 "./data:/data:ro",
#                 "ghcr.io/astral-sh/uv:alpine",
#                 "uv",
#                 "run",
#                 "--with",
#                 "pandas",
#                 "-q",
#                 "python",
#                 "-iu",
#             ],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#             text=True,
#             bufsize=0,
#             env=env,
#         )
#
#     def execute(self, code, timeout_sec=10):
#         sentinel = "###__END__###"
#         b64_code = base64.b64encode(code.encode("utf-8")).decode("utf-8")
#         wrapper = f"exec(__import__('base64').b64decode('{b64_code}'))"
#
#         try:
#             self.process.stdin.write(wrapper + "\n")
#             self.process.stdin.write(f"print('{sentinel}')\n")
#             self.process.stdin.flush()
#         except BrokenPipeError:
#             remaining_output = self.process.stdout.read()
#             return f"Error: Container died. Logs:\n{remaining_output}"
#
#         output_lines = []
#         while True:
#             line = self.process.stdout.readline()
#             if not line or sentinel in line:
#                 break
#             output_lines.append(line.rstrip())
#         return "\n".join(output_lines)
#
#
# mcp = FastMCP("DockerSandbox")
# sandbox = DockerSandbox()
#
#
# @mcp.tool()
# def execute_python(code: str) -> str:
#     """
#     Executes Python code in a persistent Docker sandbox with pandas installed.
#     State (variables, imports) persists between calls.
#     """
#     return sandbox.execute(code)
#
#
# if __name__ == "__main__":
#     mcp.run()

import base64
import os
import subprocess

from mcp.server.fastmcp import FastMCP


class DockerSandbox:
    def __init__(self):
        print("Container starting... (this may take 10-20s for the first run)")

        # Use system socket to avoid API version errors
        env = os.environ.copy()
        env["DOCKER_HOST"] = "unix:///var/run/docker.sock"

        self.process = subprocess.Popen(
            [
                "docker",
                "run",
                "--rm",
                "-i",
                "--memory=2024m",  # Bumped memory to prevent 'Container died'
                "--cpus=1.0",
                "-v",
                f"{os.getcwd()}/data:/data:ro",
                "ghcr.io/astral-sh/uv:python3.12-bookworm-slim",
                "uv",
                "run",
                "--with",
                "pandas",  # Install pandas
                "--with",
                "matplotlib",  # Install matplotlib
                "-q",  # Quiet uv
                "python",
                "-iqu",  # -i (interactive), -q (SUPPRESS STARTUP MSG), -u (unbuffered)
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr to catch installation logs
            text=True,
            bufsize=0,
            env=env,
        )
        self._wait_for_ready()
        self.execute(
            "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt"
        )

    def _wait_for_ready(self):
        """Blocks until the Python REPL is actually responsive."""
        # We send a dummy print. If we get it back, the container is alive
        # and all 'uv' installation logs are finished.
        try:
            self.process.stdin.write("print('READY')\n")
            self.process.stdin.flush()

            while True:
                line = self.process.stdout.readline()
                if "READY" in line:
                    print("Container ready!")
                    break
                if not line:
                    raise RuntimeError("Container died during startup.")
        except BrokenPipeError:
            print("CRITICAL: Container crashed. Try 'docker run' manually to debug.")
            raise

    def execute(self, code):
        sentinel = "###__END__###"
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


# Initialize sandbox IMMEDIATELY when script runs
sandbox = DockerSandbox()
mcp = FastMCP("DockerSandbox")


@mcp.tool()
def execute_python(code: str) -> str:
    """Executes Python code. Pandas and matplotlib is pre-installed."""
    return sandbox.execute(code)


if __name__ == "__main__":
    # Run as an SSE server (standalone)
    mcp.run(transport="sse")
