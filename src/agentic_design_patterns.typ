#import "theme.typ": *

#import "@preview/cetz:0.4.2"
#import "@preview/cetz-plot:0.1.3": chart, plot, smartart



/*
 * Patterns:
 *   * sequential pipeline / fixed workflow
 *       * validate, process, report
 *   * router: coordinator / dispatcher
 *   * HITL
 *   * parallel fan-out / gather
 *       * [call api1, call api2], synthesize
 *   * hierarchical decomposition
 *       * break down and delegate
 *
 *   * Review/Critique Pattern (Generator-Critic)
 *       * Improve the quality or validity of generated output by having a dedicated agent review it.
 *         * generator runs -> saves draft to state['draft_text']
 *         * reviewer runs -> reads state['draft_text'], saves status to state['review_status']
 *    * Iterative Refinement Pattern
 *        * Progressively improve a result (e.g., code, text, plan) stored in the session state until a quality threshold is met or a maximum number of iterations is reached.
 */

#imgslide(
  "Agentic Design Patterns: Sequential workflow",
  "../assets/img/bala-seq-pattern.png",
  "Source: https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns",
)

#imgslide(
  "Agentic Design Patterns: Tool use",
  "../assets/img/bala-tool-use.png",
  "Source: https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns",
)

#imgslide(
  "Agentic Design Patterns: Reflection",
  "../assets/img/bala-reflection-pattern.png",
  "Source: https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns",
)

#imgslide(
  "Agentic Design Patterns: HITL pattern",
  "../assets/img/bala-hil-pattern.png",
  "Source: https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns",
)


#imgslide(
  "Agentic Design Patterns: Planning pattern",
  "../assets/img/bala-planning-pattern.png",
  "Source: https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns",
)


#imgslide(
  "Agentic Design Patterns: Multi-agent pattern",
  "../assets/img/bala-multiagent-pattern.png",
  "Source: https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns",
)


// see this https://www.ibm.com/think/topics/react-agent
// Paper: https://arxiv.org/pdf/2210.03629
#slide[
  #title[Agentic Design Patterns: ReAct]
  #side-by-side(gutter: 3mm, columns: (1.5fr, 2fr))[
    - design pattern for agentic systems
    - builds on Chain-of-Thought prompting + tool-use
    - simple but powerful
  ][
    #figure(
      image("../assets/img/react-pattern.png", height: 70%, fit: "contain"),
      numbering: none,
      caption: [
        #set text(size: 10pt)
        M.-T. Luong. \"Neural Machine Translation\", PhD Thesis, Stanford CS Dept., 2016
      ],
    )
  ]
]

#slide[
  #title[Exercise 4]
  #set align(horizon)
  - time to build our first agent!
  - see `exercises/04_react.ipynb`
    - write from scratch
    - using langgraph
]


// #slide[
//   #title[Agentic Design Patterns: Supervisor Pattern]
//
//   #cetz.canvas({
//     import cetz.draw: *
//     // General function for curved arrows
//     let bent-arrow(from, to, label: none, bend: 1.5, a-anc: "north-east", b-anc: "north-west") = {
//       let start = from + "." + a-anc
//       let end = to + "." + b-anc
//       // Float: 15% gap from both sides
//       let s-pt = (start, 15%, end)
//       let e-pt = (start, 85%, end)
//       // Calculate Curve
//       let mid = (s-pt, 50%, e-pt)
//       let control = (rel: (0, bend), to: mid)
//       bezier(s-pt, e-pt, control, mark: (end: ">"))
//       // Smart Labeling
//       if label != none {
//         // Calculate the peak of the curve (midpoint of the quadratic bezier construction)
//         let peak = (mid, 50%, control)
//         // If bending down (negative), place text BELOW the line (anchor: north)
//         // If bending up (positive), place text ABOVE the line (anchor: south)
//         let txt-anchor = if bend > 0 { "south" } else { "north" }
//         content(peak, label, anchor: txt-anchor, padding: 0.2em)
//       }
//     }
//
//     set text(size: 1pt)
//
//     content((0, 0), [User], frame: "circle", padding: 1em, name: "user")
//     content((6, 0), [Main Agent], frame: "circle", padding: 1em, name: "agent")
//     content((12, 8), [Subagent 1], frame: "circle", padding: 1em, name: "sa1")
//     content((12, 4), [Subagent 2], frame: "circle", padding: 1em, name: "sa2")
//     content((12, 0), [Subagent 3], frame: "circle", padding: 1em, name: "sa3")
//     bent-arrow("user", "agent", label: [ ], bend: 0, a-anc: "east", b-anc: "west")
//   })
//
// ]
//

// #slide[
//   #title[Agentic Design Patterns: Supervisor Pattern]
//   #set text(size: 15pt)
//   ```python
//
//   # Define subagents (e.g., research and writing specialists)
//   research_agent = create_agent(model="gpt-4o", prompt="You are a research specialist...")
//   writer_agent = create_agent(model="gpt-4o", prompt="You are a writing specialist...")
//
//   # Registry of available subagents
//   SUBAGENTS = { "research": research_agent, "writer": writer_agent, }
//
//   @tool
//   def task(agent_name: str, description: str) -> str:
//       """Launch an ephemeral subagent for a task."""
//       agent = SUBAGENTS[agent_name]
//       result = agent.invoke({"messages": [{"role": "user", "content": description}]})
//       return result["messages"][-1].content
//
//   # Main coordinator agent
//   main_agent = create_agent(
//       model="gpt-4o",
//       tools=[task],
//       system_prompt="You coordinate sub-agents. Available: research, writer. Use the task tool ...."
//   )
//   ```
// ]

