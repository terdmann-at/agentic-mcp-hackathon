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

// #slide()[
//   #title[Shouldn't GDP go up?]
//   #set text(size: 15pt)
//   #block(inset: 2em)[
//     #side-by-side(gutter: 3mm, columns: (1fr, 2fr))[
//       #one-by-one[
//         Andrey Karpathy's take:
//         #list(marker: [#bullet()])[
//           did not happen for computers, mobile phones either
//         ]
//       ][
//         #list(marker: [#bullet()])[
//           actual changes are more gradual, averaged out over longer time
//         ]
//       ][
//         #list(marker: [#bullet()])[
//           we will just have more automation / we can write programs that we could not write before
//         ]
//       ]
//     ][
//       #set align(center + horizon)
//       #figure(image("/assets/img/Screenshot 2025-12-21 at 12.35.46.png", width: 100%))
//     ]
//   ]
// ]

// #slide[
//   #title[Progress on the path to AGI]
//   #figure(
//     image(
//       "/assets/img/Screenshot 2025-12-19 at 20.03.44.png",
//       width: 90%,
//       height: 80%,
//       fit: "contain",
//     ),
//   ) <agi>
// ]

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
  [Databricks],
  [Clone the repo at: "https://github.com/terdmann-at/agentic-mcp-hackathon.git"],
)


