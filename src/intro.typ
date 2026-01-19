#import "theme.typ": *

#slide[
  #title[Gartner Hype Cycle]

  #only(1)[
    #set align(horizon)
    #figure(
      image(
        "/assets/img/Figure_1_Hype_Cycle_for_Artificial_Intelligence_2023.png",
        width: 80%,
        height: 80%,
        fit: "contain",
      ),
    )]

  #only(2)[
    #set align(horizon)
    #figure(
      image(
        "/assets/img/Figure_1_Hype_Cycle_for_Artificial_Intelligence_2025.png",
        width: 80%,
        height: 80%,
        fit: "contain",
      ),
    )]

  #only(3)[
    #set align(center + horizon)
    #block(inset: 3em)[
      "Despite an average spend of \$1.9 million on GenAI initiatives in 2024, less
      than 30% of AI leaders report their CEOs are happy with AI investment return.
      Low-maturity organizations have trouble identifying suitable use cases and
      exhibit unrealistic expectations for initiatives. Mature organizations,
      meanwhile, struggle to find skilled professionals and instill GenAI literacy."
    ]
  ]
]

#imgslide("A. Karpathy on programming", "/assets/img/Screenshot 2025-12-29 at 22.44.35.png", "")

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

#slide()[
  #title[Shouldn't GDP go up?]

  #set text(size: 15pt)
  #block(inset: 2em)[

    #side-by-side(gutter: 3mm, columns: (1fr, 2fr))[

      #one-by-one[
        Andrey Karpathy's take:
        #list(marker: [#bullet()])[
          did not happen for computers, mobile phones either
        ]
      ][
        #list(marker: [#bullet()])[
          actual changes are more gradual, averaged out over longer time
        ]
      ][
        #list(marker: [#bullet()])[
          we will just have more automation / we can write programs that we could not write before
        ]
      ]

    ][
      #set align(center + horizon)
      #figure(image("/assets/img/Screenshot 2025-12-21 at 12.35.46.png", width: 100%))
    ]
  ]
]

#slide[
  #title[Progress on the path to AGI]

  #figure(
    image(
      "/assets/img/Screenshot 2025-12-19 at 20.03.44.png",
      width: 90%,
      height: 80%,
      fit: "contain",
    ),
  ) <agi>
]

#slide[
  #title[Measuring AI Ability to Complete Long Tasks]
  #figure(
    image(
      "/assets/img/Screenshot 2025-12-21 at 14.03.25.png",
      // "assets/difficulty-model-perf.png",
      width: 90%,
      height: 80%,
      fit: "contain",
    ),
  ) <longtasks>
]

// #let list-slide(title-text, ..items) = slide[
//   #title[#title-text]
//   #set align(horizon)
//   // 1. Force all lists (nested included) to use this marker
//   #set list(marker: bullet())
//
//   #block(inset: 3em)[
//     #one-by-one(
//       ..items
//         .pos()
//         .map(item => {
//           // 2. Wrap the top-level arguments in a list item
//           list(item)
//         }),
//     )
//   ]
// ]

#list-slide(
  "Agentic AI and MCP Workshop",
  [Why are you here?],
  [What experiences do you have with:],
  indent[LLMs], // Formatter can't break this
  indent[Agents],
  indent[MCP],
)

#list-slide(
  "Agentic AI and MCP Workshop",
  [The goals of this workshop],
  indent[Review LLM basics],
  [LLM Agents concepts],
  indent[Tool calling + Code execution], // Formatter can't break this
  indent[Workflows, Orchestration, Autonomy],
  [MCP],
  indent[Clients + Servers],
)

#list-slide(
  "Agentic AI and MCP Workshop",
  [What we will do:],
  indent[Theory / concepts],
  indent[Coding exercises],
  indent[Lab sessions + try out your own ideas],
)

#list-slide(
  "Setup Hackathon",
  [git + github account],
  [ python + uv],
  [ IDE],
  [codespaces],
)


