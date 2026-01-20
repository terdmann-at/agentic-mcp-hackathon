
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
// #set text(size: 20pt, font: "Google Sans Flex 120pt", fill: black)
// #set text(size: 20pt, font: "Apple SD Gothic Neo", fill: black)
// #set text(size: 20pt, font: "Iosevka NF", fill: black)


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
  - check out the code at `labs/lab_01_deep_research.ipynb`
  - Tasks:
    - code up a deep-research system
    - evaluate your system and compare with react agent
    - what works better?
]

#my-new-section("Lunch", "12.00")

#include "mcp.typ"

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

#slide[
  #title[Advanced Concepts: Coding agents]
  #block(inset: 2em)[
    #item-by-item[
      - LLMs are good at code. Why must tool-calls be written in JSON?
      - https://blog.cloudflare.com/code-mode/: #block(inset: 1em)[
          #set text(size: 15pt)
          "[...] We tried something different: Convert the MCP tools into a TypeScript API, and then ask an LLM to write code that calls that API. [...]
          We found agents are able to handle many more tools, and more complex tools, when those tools are presented as a TypeScript API rather than directly."
          [...]
          The approach really shines when an agent needs to string together multiple calls. With the traditional approach, the output of each tool call must feed into the LLM's neural network, just to be copied over to the inputs of the next call, wasting time, energy, and tokens. When the LLM can write code, it can skip all that, and only read back the final results it needs.
        ]
      - `smolagents` library is based on this pattern
    ]
  ]
]


#imgslide(
  "Code agent",
  "/assets/img/code_agent.png",
  "Source: https://huggingface.co/blog/open-deep-research#the-gaia-benchmark",
)

#imgslide(
  "Magentic One",
  "../assets/img/magentic_orchestrator.png",
  "Source: https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/",
)


#slide[
  #title[Advanced Concepts: Memory]
  #block(inset: 2em)[
    #item-by-item[
      - in principle, memory allows the agent to self-improve
      - in practice, no one knows yet how to best make use of it
      - https://github.com/letta-ai/letta
      - again, we can use tools:
        - create memory after learning something
        - recall memories given some query
    ]
  ]
]


#slide[
  #title[Exercise 06: Code execution and memory]
  #block(inset: 2em)[
    - see `exercises/06_code_execution.ipynb`
    - Goals:
      - build a simple data analysis agent
      - give the agent memory
  ]
]


#slide[
  #title[Exercise 06: Code execution and memory]
  #block(inset: 2em)[
    - see `exercises/07_coding-agent.ipynb`
    - Goals:
      - build a simple data analysis agent
      - give the agent memory
  ]
]

#slide[
  #title[The Risk: "What is the worst that can happen?"]
  #block(inset: 1em)[
    Even with Docker, a malicious or confused agent with root inside a container can cause damage if not properly sandboxed:
    #item-by-item[
      - Host Filesystem Wipe: If mounting `-v ./data:/data` and the agent runs `rm -rf /data/*`: this deletes the files on your actual laptop/server
      - Network Attacks: The agent can use curl or Python to scan your local network (192.168.1.x), attack other devices, or access internal services (like a local database) that have no password.
      - Resource Exhaustion (DoS): The agent could launch a "fork bomb" or fill the disk, crashing your host machine.
      - Container Escape (Rare): If there is a kernel vulnerability, running as root increases the chance of "escaping" the container to control the host OS.
    ]
  ]
]


#slide[
  #title[The Risk: "Lethal trifecta"]
  #block(inset: 2em)[
    #item-by-item[
      1. Access to private data
      2. Ability to externally communicate
      3. Exposure to untrusted content
    ]
  ]
]


#imgslide(
  "Multimodal LLMs",
  "../assets/img/multimodal-llms-1.jpg",
  "Source: https://magazine.sebastianraschka.com/p/understanding-multimodal-llms",
)

#slide[
  #title[Exercise 08: Image Understanding]
  #block(inset: 2em)[
    - see `exercises/08_image_understanding.ipynb`
  ]
]


#slide[
  #title[Advanced Concepts: Deep Agents]
  #block(inset: 1em)[
    #item-by-item[
      - Agents can increasingly tackle long-horizon tasks
        - agent task length doubling every 7 months
      - But: long horizon tasks often span dozens of tool calls, which present cost and reliability challenges.
      - Popular agents such as Claude Code and Manus use some common principles to address these challenges, including:
        - planning (prior to task execution)
        - computer access (giving the agent access to a shell and a filesystem)
        - sub-agent delegation (isolated task execution)

    ]
  ]
]

#slide[
  #title[Advanced Concepts: RLM]
  #side-by-side(gutter: 3mm, columns: (1.5fr, 2fr))[
    #block(inset: 1em)[
      #item-by-item[
        - Another recent innovation: Recursive Language Models (RLMs)
        - RLM provides the illusion of near infinite context
        - under the hood a language model manages, partitions, and recursively calls itself or another LM over the context accordingly to avoid context rot
      ]
    ]
  ][
    #figure(
      image("../assets/img/RLM-1.png", width: 80%),
      numbering: none,
      caption: [
        #set text(size: 8pt)
        "Source: https://alexzhang13.github.io/blog/2025/rlm/"
      ],
    )
  ]
]


// #my-new-section("Coffee break 2", "15.00")

#my-new-section("Lab 2: MCP + advanced agents", "15.15")

#slide[
  #title[Lab 2: Building a deep-agent with MCP]
  #set align(horizon)
  - see the starter code at `labs/lab_02_advanced.ipynb`
  - Tasks:
    - implement a MAS with coding and web-search sub-agents
    - use the "progressive disclosure" pattern
    - evaluate your system
  - Bonus: Allow the system "to see".
  - Bonus: Try evaluating against hard GAIA questions.
]


#my-new-section("Conclusion", "16.45")

#slide[
  #title[Conclusion]
  #set align(horizon)
  #block(inset: 2em)[
    #item-by-item[
      - Some fun: https://gricha.dev/blog/the-highest-quality-codebase
      - Future trends:
        - David Silver:
          - "models will be trained with RL for computer use"
          - "with this the models will go beyond human data: era of experience"
      - Feedback
    ]
  ]
]

// TODO: summarize the below:
// https://x.com/karpathy/status/2002118205729562949?s=20
#slide()[
  #title[A. Karpathy's 2025 LLM Year in Review]
  - Rise of RLVR (Reinforcement Learning from Verifiable Rewards): The standard training pipeline (Pretraining → SFT → RLHF) has evolved. The new key stage is RLVR, where models train against verifiable outcomes (like math or code execution). This allows them to "think" longer and develop reasoning strategies, similar to OpenAI's o1 and o3 models.
  - "Jagged" Intelligence (Ghosts vs. Animals): Karpathy describes current AI as "ghosts" rather than "animals." Because they are not evolved for biological survival but optimized for specific rewards, their intelligence is "jagged"—they can be geniuses at complex tasks but fail at basic common sense or be easily "jailbroken."
  - Vibe Coding: A shift in programming where users simply describe what they want in natural language ("vibes"), and the AI handles the actual implementation. This lowers the barrier to entry, allowing non-coders to build software and professionals to work faster.
  - The App Layer (e.g., Cursor): A distinct "application layer" is emerging (like the Cursor IDE) that acts as a manager for the raw "college graduate" intelligence of LLMs. These apps handle context, tools, and the feedback loop to make the models actually useful for work.
  - Benchmark Fatigue: There is growing skepticism toward standard benchmarks. Since models are now heavily optimized (or "benchmaxxed") for specific test sets, high scores no longer guarantee real-world utility.
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
