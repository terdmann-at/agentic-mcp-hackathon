
#import "theme.typ": *

// Make the paper dimensions fit for a presentation and the text larger
#set page(
  paper: "presentation-16-9",
  margin: (x: 1em, y: 1em),
  // background: box(fill: rgb("#222222"), width: 100%, height: 100%),
  background: box(fill: rgb("#eeeeee"), width: 100%, height: 100%),
  // margin: (x: 4em, y: 2em),
)

#set text(size: 20pt, font: "Helvetica Neue", fill: black)


#slide[

  #set page(
    margin: (x: 2em, y: 1em),
    background: image("/assets/at-bg.jpg", width: 100%, height: 100%, fit: "cover"),
  )
  #place(top + left, dx: 0pt, dy: 10pt)[
    #image("/assets/at-logo.png", width: 4cm)
  ]
  #v(3cm)

  #set text(size: 30pt)
  #set align(horizon)
  #title[Workshop: Agentic AI and MCP]

  #set text(size: 20pt, fill: white)
  Tore Erdmann

  #set text(fill: sunset-gradient)
  Altana | 21.01.2026
]


#my-new-section("Introduction", "09:00")
#include "intro.typ"

#my-new-section("LLM basics", "09.15")
#include "llm_basics.typ"

#my-new-section("Agents", "10.00")
#include "agents.typ"


#my-new-section("Lab 1: Deep research", "11.00")

#slide[
  #title[Deep-research system]

  - GAIA is arguably the most comprehensive benchmark for agents
  - Its questions are very difficult and hit on many challenges of LLM-based systems
  - Here is an example of a hard question:
    #box(inset: 1em)[
      #set text(size: 0.8em)
      Which of the fruits shown in the 2008 painting "Embroidery from Uzbekistan" were served as part of the October 1949 breakfast menu for the ocean liner that was later used as a floating prop for the film "The Last Voyage"? Give the items as a comma-separated list, ordering them in clockwise order based on their arrangement in the painting starting from the 12 o'clock position. Use the plural form of each fruit.
    ]
  - OpenAI reported that GPT-4 only got 7% correct, while their deep-research system got 67%
]

#slide[
  #title[Lab 1: Building a deep-research system]
  #set align(horizon)
  - we are ready for our first project
  - see the starter code at `code/deep-research/`
  - Tasks:
    - code up a deep-research system
    - evaluate your system and compare with react agent
    - what works better?
  - https://github.com/Ayanami0730/deep_research_bench
]

#my-new-section("Lunch", "12.00")

#my-new-section("MCP", "13.00")

#slide[
  #title[Model Context Protocol (MCP)]

  One year of MCP:
  - first released Nov 24
  - supports tools, resources and prompts
    - exetuble actions (API calls, running scripts)
    - local files, db queries, cloud documents etc.
    - structured prompts
  - donated to Linux Foundation
  - see https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
]

#slide[
  #title[Why use MCP?]
  - interoperability: solves the NxM problem
  - reusing toolsets across different agents with slightly different APIs
  - not required for tool calling: list of available tools it provided to LLM with every request
]



#slide[
  #title[Downsides of MCP]
  - slower than calling a tool locally (needs network request etc)
  - letting agents write code to compose MCP much more effective
  - and much more token efficient
  - MCP offers no way for servers to declare their runtime/dependency needs
  - Since tools are drawn from arbitrary sources, they are not aware of what other tools are available to the agent. Their instructions can't account for the rest of the toolbox
  - Agents tend to be less effective at tool use as the number of tools grows
]


// TODO: fill this in
#slide[
  #title[Exercise X]
  #item-by-item[
    - see `notebooks/XX_mcp.py`
      - connect to MCP server
      - write MCP server
  ]
]

#slide[
  #title[Dynamic MCP]
  - one problem with MCP: too many tools call overwhelm the model
  - fixed toolset
  - instead: https://www.docker.com/blog/dynamic-mcps-stop-hardcoding-your-agents-world/

  #text(size: 8pt)[
    #table(
      columns: (auto, 1fr, 1fr, 1fr),
      inset: 10pt,
      align: horizon,
      table.header([*Workflow*], [*Before: Static MCP setup*], [*After: Dynamic MCPs*], [*Impact*]),
      [Tool discovery],
      [Manually browse the MCP servers],
      [mcp-find searches a Docker MCP Catalog (230+ servers)],
      [Faster discovery],

      [Adding tools],
      [Enable the MCP servers manually],
      [mcp-add pulls only the servers an agent needs],
      [Zero manual config; just-in-time tooling],

      [Authentication],
      [Configure the MCP servers ahead of time],
      [Prompt user to complete OAuth when required],
      [Smoother onboarding flows (mcp-ui)],

      [Tool composition],
      [Agent generated tool calls; definitions sent to model],
      [With code-mode, agents write code using multiple tools],
      [Multi-tool workflows and unified outputs],

      [Context size],
      [Load lots of unused tool definitions],
      [Keep only the tools actually required for the task],
      [Lower token usage and latency],

      [Future-proofing],
      [Static integrations],
      [Dynamic, composable tools with sandboxed scripting],
      [Ready for evolving agent behaviors],

      [Developer involvement],
      [Constant context switching and config hacking],
      [Agents self-serve: discover, authorize, and orchestrate],
      [Fewer manual steps; better focus time],
    )
  ]
]

#my-new-section("Agents: Advanced Concepts", "14.00")

#imgslide(
  "Code agent",
  "/assets/img/code_agent.png",
  "Source: https://huggingface.co/blog/open-deep-research#the-gaia-benchmark",
)


#slide[
  #title[Advanced Concepts: Memory]
  - memory allows the agent to self-improve
  - let's build a memory tool
  - https://github.com/letta-ai/letta
]

#slide[
  - Exercise: deep coding agent with memory
  - use to analyze data?
  - remember what has been tried before
]

#slide[
  #title[Advanced Concepts: Deep Agents]
  - agent with shell and code execution
  - Recursive Language Models
  - Agents can increasingly tackle long-horizon tasks, with agent task length doubling every 7 months! But, long horizon tasks often span dozens of tool calls, which present cost and reliability challenges. Popular agents such as Claude Code and Manus use some common principles to address these challenges, including planning (prior to task execution), computer access (giving the agent access to a shell and a filesystem), and sub-agent delegation (isolated task execution).
]

#slide[
  #title[The Risk: "What is the worst that can happen?"]
  #block(inset: 2em)[
    #item-by-item[
      Even with Docker, a malicious or confused agent with root inside a container can cause damage if not properly sandboxed:
      - Host Filesystem Wipe: You mounted `-v ./data:/data`. If the agent runs `rm -rf /data/*`, it deletes the files on your actual laptop/server.
      - Network Attacks: The agent can use curl or Python to scan your local network (192.168.1.x), attack other devices, or access internal services (like a local database) that have no password.
      - Resource Exhaustion (DoS): The agent could launch a "fork bomb" or fill the disk, crashing your host machine.
      - Container Escape (Rare): If there is a kernel vulnerability, running as root increases the chance of "escaping" the container to control the host OS.
    ]
  ]
]

#slide[
  #title[The Risk: "Lethal trifecta"]
  1. Access to private data
  2. Ability to externally communicate
  3. Exposure to untrusted content
]



// #my-new-section("Coffee break 2", "15.00")

#my-new-section("Lab 2: MCP + advanced agents", "15.15")

#slide[
  #title[Lab 2: Building a deep-agent with MCP]
  #set align(horizon)
  - see the starter code at `exercises/lab_02_mcp_advanced/`
  - Tasks:
    - implement a coding-agent
    - build a deep-agent that can delegate coding tasks to the coding-agent
    - evaluate your system
  - Bonus: Allow the system "to see"
]


#my-new-section("Conclusion", "16.45")

#slide[

  #set align(horizon)

  Some fun:
  - https://gricha.dev/blog/the-highest-quality-codebase

  Future trends:
  - Small models like HRM are not frontier models (1-2 trillion paramters), but can do reasoning
  - David Silver:
    - "models will be trained with RL for computer use"
    - with this the models will go beyond human data ("era of experience")
  - RLMs: https://alexzhang13.github.io/blog/2025/rlm/

  - More readings: https://arxiv.org/html/2401.03428v1
]

// /*
// = Appendix
//
// == Basics: MLP
//
// - First neural networks: Perceptrons
// - Basically deterministic logistic regression $ f(x_i; θ) = I(w^T x_i + b > 0) $
//
// #pause
//
// #figure(
// image("/assets/img/Screenshot 2025-12-19 at 19.23.55.png", width: 80%),
// ) <perc>
//
// == Basics: MLP
//
// - MLP $ f(x_i; θ) = sigma (w^T x_i + b) $
// - zl = fl(zl−1) = φl(bl + Wlzl−1)
// - One can show that an MLP with one hidden layer is a universal function approximator
// - deep networks work better than shallow ones due to composition
// - explosion of DNN: availability of cheap GPUs (graphics processing units)
//
// == Basics: MLP
//
// == A short History
//
// - RNN-based language models
// - 2017 Transformer architecture gets published
// - 2021 GPT-1
// - 2023 ChatGPT
// - 2024 GPT-4
// - 2025 GPT-5, Gemini 3.0, etc.
// - Feb 2025 - Claude Code
//
// == GPT-1
//
// #figure(
// image("/assets/img/gpt1_paper.png", width: 80%),
// caption: [],
// ) <gpt1>
// */
