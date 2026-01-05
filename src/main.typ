/*
 *
 *
 * Exercises:
 *   - 01: Chatbot
 *   - 02: RAG
 *   - 03: Tool-calling / RAG via tool-calling
 *   - 04: ReAct
 *   - 05: More agentic design patterns
 *
 *
 */

#import "logic.typ": *
#import "toolbox.typ": *

// Make the paper dimensions fit for a presentation and the text larger
#set page(
  paper: "presentation-16-9",
  margin: (x: 1em, y: 1em),
  // background: box(fill: rgb("#222222"), width: 100%, height: 100%),
  background: box(fill: rgb("#eeeeee"), width: 100%, height: 100%),
  // margin: (x: 4em, y: 2em),
)

// #let title-slide(title_txt) = {
//   slide[
//     #set align(center + horizon)
//     #title[#title_txt]
//     #toolbox.register-section[#title_txt]
//   ]
// }


// #let sections-band = toolbox.all-sections((sections, current) => {
//   set text(fill: gray, size: .8em)
//   sections.map(s => if s == current { strong(s) } else { s }).join([ • ])
// })
// #set page(footer: sections-band)

#set text(size: 20pt, font: "Helvetica Neue", fill: black)

#let sunset-gradient = gradient.linear(
  // cmyk(0%, 27%, 50%, 0%),
  // cmyk(0%, 78%, 88%, 0%),
  // color.hsl(28deg, 44%, 60%), // orig
  // color.hsl(13deg, 81%, 60%), // orig
  // color.hsl(28deg, 74%, 51%),
  // color.hsl(13deg, 95%, 50%),
  color.hsl(32deg, 74%, 60%),
  color.hsl(13deg, 95%, 50%),
)

#let sunset-gradient-2 = gradient.linear(
  color.hsl(32deg, 74%, 60%).transparentize(90%),
  color.hsl(13deg, 95%, 50%).transparentize(90%),
  relative: "parent",
)

#let sunset-gradient-3 = gradient.linear(
  color.hsl(32deg, 74%, 60%).transparentize(98%),
  color.hsl(13deg, 95%, 50%).transparentize(98%),
  relative: "parent",
)

#let black-gradient = gradient.linear(
  rgb("#000000").transparentize(90%),
  rgb("#000000").transparentize(20%),
  rgb("#000000").transparentize(10%),
  rgb("#000000").transparentize(10%),
  rgb("#000000").transparentize(10%),
)


// #let bullet() = {
//   #text(white)[#sym.circle.filled]
// }
#let bullet-color = color.hsl(13deg, 95%, 50%).transparentize(10%)
#let bullet() = {
  text(bullet-color)[#sym.circle.filled]
}

#let title(body) = {
  box(
    stroke: 6pt + sunset-gradient-3,
    inset: 0.0em,
  )[
    #box(stroke: 4pt + sunset-gradient-2, inset: 0.0em)[
      #box(stroke: 1pt + sunset-gradient, inset: 0.0em)[
        #box(
          stroke: 0.3pt + white.transparentize(50%),
          inset: 0.5em,
        )[
          #text(fill: sunset-gradient, weight: "bold")[
            #heading(level: 1, body)
          ]
        ]
      ]
    ]
  ]
}

#let imgslide(title_txt, impath, caption) = {
  slide()[
    #title[#title_txt]
    #figure(image(impath, height: 80%, fit: "contain"), numbering: none, caption: [
      #set text(size: 10pt)
      #caption
    ])
  ]
}
// Usage
// #imgslide("test title", "assets/RAG_diagram.svg", "test")

#let list-slide(title-text, ..items) = slide[
  #title[#title-text]
  #set align(horizon)
  #block(inset: 3em)[
    #one-by-one(
      // Transform each item into a list block
      ..items
        .pos()
        .map(item => {
          list(marker: bullet())[#item]
        }),
    )
  ]
]

// #let my-new-section(name, time) = slide[
//   #set align(center + horizon)
//   #set text(fill: sunset-gradient, weight: "bold")
//   // 1. Create the look for the Table of Contents entry here
//   #let toc-entry = [
//     #name
//     #h(1fr) // Spacer
//     #text(size: 0.7em, weight: "thin")[#time] // Formatting for time
//   ]
//   // 2. Register the pre-formatted content
//   #register-section(toc-entry)
//   #box(
//     stroke: 6pt + sunset-gradient-3,
//     inset: 0.0em,
//   )[
//     #box(stroke: 4pt + sunset-gradient-2, inset: 0.0em)[
//       #box(stroke: 1pt + sunset-gradient, inset: 0.0em)[
//         #box(
//           stroke: 0.3pt + white.transparentize(50%),
//           inset: 0.5em,
//         )[
//           // 3. Only display the name in the big heading
//           #heading(level: 1, name)
//         ]
//       ]
//     ]
//   ]
// ]

// #let sunset-gradient = gradient.linear(
//   // focal-center: (10%, 10%),
//   // focal-radius: 25%,
//   // angle: 0deg,
//   // rgb("#ffeb80"),
//   rgb("#fbeb60"),
//   // rgb("#d0b55b"),
//   // rgb("#fb002f"),
//   rgb("#fba52b"),
//   // rgb("#fba52b"),
//   rgb("#fb002f"),
//   // focal-center: (20%, 40%),
//   // focal-radius: 15%,
//   relative: "parent",
// )



// Use #slide to create a slide and style it using your favourite Typst functions
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

#let my-new-section(name, time) = slide[
  // 1. Define the formatted content for the list
  #let toc-entry = [
    #name
    #h(1fr)
    #text(size: 0.8em, weight: "regular")[#time]
  ]

  // 2. Register it
  #register-section(toc-entry)

  // 3. Page / Background setup
  #set page(margin: (x: 0em, y: 0em), background: image(
    "/assets/at-bg.jpg",
    width: 100%,
    height: 100%,
    fit: "cover",
  ))
  #place(top + left, box(fill: black-gradient, width: 100%, height: 100%))

  #box(height: 100%, clip: true)[
    // 4. Content
    #block(inset: (x: 2em, y: 1em))[
      #title[Agenda] // Or use your nested box design here if preferred
      #v(-3em)
      #set text(fill: white)

      #side-by-side(gutter: 3mm, columns: (1.5fr, 2fr))[
        // Left column content (optional)
      ][
        #set align(horizon)
        #all-sections((sections, current) => {
          // 5. Map sections to apply fading logic
          let formatted-items = sections.map(section => {
            if section == current {
              // Highlight: Full opacity, bold
              text(weight: "bold", section)
            } else {
              // Inactive: Fade out
              text(fill: white.transparentize(70%), weight: "regular", section)
            }
          })

          // 6. Display the list
          enum(
            numbering: n => block(text(fill: sunset-gradient, weight: "bold", size: 25pt)[#n]),
            tight: false,
            body-indent: 2em,
            ..formatted-items,
          )
        })
      ]
    ]
  ]
]

#my-new-section("Introduction", "09:00")

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

// 1. A clearer way to signal indentation
#let indent(body) = (type: "indent", body: body)

#let list-slide(title-text, ..items) = slide[
  #title[#title-text]
  #set align(horizon)
  #set list(marker: bullet())

  #block(inset: 3em)[
    #one-by-one(
      ..items
        .pos()
        .map(item => {
          if type(item) == dictionary and item.at("type", default: none) == "indent" {
            pad(left: 1.5em, list(item.body))
          } else {
            list(item)
          }
        }),
    )
  ]
]

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

#let title-slide(title_txt) = {
  slide[
    #set align(center + horizon)
    #title[#title_txt]
    #register-section[#title_txt]
  ]
}

#my-new-section("LLM basics", "09.15")



#slide[
  #title[How does text-generation with LLMs work?]
  #set align(horizon)
  #item-by-item[
    - given some words $w_1, w_2, ..., w_t$, LLMs predict the probability of the next word $w_(t+1)$
    - LLMs are a model of: $ P_theta (w_(t+1) | w_1, w_2, ..., w_t) $
    - the model weights $theta$ are pre-trained on huge amounts of text
    - and then trained some more (post-training) to follow instructions
    - the words $w_1, ...$ are the "prompt" and allow us to use the model
  ]
]

#let inverted-image(path) = {
  // This logic applies a visual inversion filter
  set image(color-filter: c => c.negate())
  image(path)
}
#slide[
  #set align(center + horizon)
  #only(1)[#grid(
      columns: (auto, auto, auto, auto, auto, auto),
      align: center + horizon,
      row-gutter: 3em,
      column-gutter: 50pt,
    )[Prompt][Model][Vocabulary][ ][Probabilities][Sample][
      I am giving a ...
    ][
      #box(
        stroke: none,
        inset: 0pt,
        image("/assets/img/neural-network.png"),
      )
    ][
      #stack(spacing: 1em, dir: ttb, text()[talk], text()[green], text()[chair], text()[but], text()[...])
    ][
      #stack(spacing: 1em, dir: ttb, sym.arrow, sym.arrow, sym.arrow, sym.arrow, sym.arrow)
    ][
      #stack(spacing: 1em, dir: ttb, text(weight: "bold")[0.90], text()[0.6], text()[0.75], text()[0.01], text()[...])
    ][
      #stack(spacing: 1em, dir: ttb, text(weight: "bold")[talk], text()[ ], text()[ ], text()[ ], text()[ ])
    ]
  ]

  #only(2)[#grid(
      columns: (auto, auto, auto, auto, auto, auto),
      align: center + horizon,
      row-gutter: 3em,
      column-gutter: 50pt,
    )[Prompt][Model][Vocabulary][ ][Probabilities][Sample][
      I am giving a talk...
    ][
      #box(
        stroke: none,
        inset: 0pt,
        image("/assets/img/neural-network.png"),
      )
    ][
      #stack(spacing: 1em, dir: ttb, text()[choice], text()[about], text()[especially], text()[cellar], text()[...])
    ][
      #stack(spacing: 1em, dir: ttb, sym.arrow, sym.arrow, sym.arrow, sym.arrow, sym.arrow)
    ][
      #stack(spacing: 1em, dir: ttb, text()[0.12], text(weight: "bold")[0.91], text()[0.43], text()[0.01], text()[...])
    ][
      #stack(spacing: 1em, dir: ttb, text()[ ], text(weight: "bold")[about], text()[ ], text()[ ], text()[ ])
    ]
  ]
]

#slide[
  #title[Sequence-to-sequence models]
  #figure(
    image("/assets/img/Screenshot 2025-12-21 at 16.15.47.png", height: 70%, fit: "contain"),
    numbering: none,
    caption: [
      #set text(size: 10pt)
      M.-T. Luong. \"Neural Machine Translation\", PhD Thesis, Stanford CS Dept., 2016
    ],
  )
]

#slide[
  #box(height: 100%, clip: true)[
    #title[Attention]
    #side-by-side[
      #set text(size: 16pt)
      #item-by-item[
        - a seq to seq model: $h^d_t = f_d (h^d_(t−1),y_(t−1),c)$
        - we can set $c = h^e_t$, so the final state of the encode
        - $tilde(h)_t = tanh(W_c [c_t; h_t])$
        - this can result in poor performance, since the output does not have access to the input words themselves
        - we are compressing alot of measing into a single vector
        - we can avoid this bottleneck by allowing the output words to directly “look at” the input words
        - use dynamic context vector: $ c_t = sum_(i=1)^T alpha_i (h^d_(t-1), h^e_(1:T)) h^e_i $
        - this is a weighted mean (soft dictionary look-up)
      ]
    ][
      #figure(
        image("/assets/img/Screenshot 2025-12-21 at 16.27.44.png", height: 70%, fit: "contain"),
        numbering: none,
        caption: [
          #set text(size: 10pt)
          M.-T. Luong. \"Neural Machine Translation\", PhD Thesis, Stanford CS Dept., 2016
        ],
      )
    ]
  ]
]

#slide[
  #figure(
    image("/assets/img/Screenshot 2025-12-30 at 14.49.02.png", height: 90%, fit: "contain"),
    numbering: none,
    caption: [
      #set text(size: 10pt)
      Illustration of the attention heatmaps generated while translating a sentence from German to English.
      From M.-T. Luong. \"Neural Machine Translation\", PhD Thesis, Stanford CS Dept., 2016
    ],
  )
]

#slide[
  #title[Transformer]
  #figure(image("/assets/img/Screenshot 2025-12-22 at 09.17.15.png", height: 80%, fit: "contain"))
]

#slide[
  #title[RLHF]
  #figure(image("/assets/img/RLHF_diagram.svg", height: 80%, fit: "contain"))
]


#slide[
  #title[Building Chatbots]
  // #set align(horizon)
  #grid(inset: (x: 1em), columns: (1fr, 1fr), column-gutter: 1em)[
    Request to OpenAI *Completions* API:
    #set text(size: 0.8em)
    ```shell
    curl https://api.openai.com/v1/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d '{
        "model": "gpt-3.5-turbo-instruct",
        "prompt": "Say this is a test",
        "max_tokens": 7,
        "temperature": 0
      }'
    ```
  ][
    And you'd get back this:
    #set text(size: 0.7em)
    ```shell
      {
        "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
        "object": "text_completion",
        "created": 1589478378,
        "model": "gpt-3.5-turbo-instruct",
        "system_fingerprint": "fp_44709d6fcb",
        "choices": [
          {
            "text": "\n\nThis is indeed a test",
            "index": 0,
            "logprobs": null,
            "finish_reason": "length"
          }
        ],
        "usage": {
          "prompt_tokens": 5,
          "completion_tokens": 7,
          "total_tokens": 12
        }
      }
    ```
  ]
]

#slide[
  #title[Building Chatbots]
  #set align(horizon)
  #block(inset: (x: 1em))[
    For the *Chat Completions* API, we send/recieve a list of messages:
    #set text(size: 0.9em)
    ```shell
    curl https://api.openai.com/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d '{
        "model": "gpt-5.2",
        "messages": [
          {
            "role": "developer",
            "content": "You are a helpful assistant."
          },
          {
            "role": "user",
            "content": "Hello!"
          }
        ]
      }'
    ```
  ]
]

#slide[
  #title[Building Chatbots]
  #set align(horizon)
  - we can call the OpenAI API to get a completion
  - how to we have a conversation?

  // #reveal-code(lines: (1, 3, 6, 7))[```python
  //     model = ChatOpenAI()
  //     response = model.invoke("Hi")
  //     response[""]
  // ```]

  ```python
      model = ChatOpenAI()
      response = model.invoke("Hi")
      print(response.content)
  ```
]

#slide[
  #title[Exercise 1]
  #block(inset: (x: 3em, y: 1em))[
    - see `notebooks/chatbot.py`
    - expected time: 10 min
  ]
]


#slide[
  #title[Retrieval Augemented Generation]
  #figure(image("/assets/img/RAG_diagram.svg", height: 80%, fit: "contain"), numbering: none, caption: [
    #set text(size: 10pt)
    Source: https://en.wikipedia.org/wiki/Retrieval-augmented_generation#/media/File:RAG_diagram.svg (retrieved on 29.12.2025)
  ])
]


#slide[
  #title[Exercise 2]
  #block(inset: (x: 3em, y: 1em))[
    - see `notebooks/rag.py`
    - expected time: 10 min
  ]
]


#my-new-section("Agents", "10.00")

#slide[
  #title[What does agentic mean?]
  #only(2)[
    #figure(
      image("/assets/img/Screenshot 2025-12-19 at 19.59.31.png", width: 80%),
    ) <agentic>
  ]
]
/*
 * Write an essay on topic X
 * Agentic:
 *   - do you need to do research (web)?
 *   - write first draft
 *   - consider which parts need revision or more research
 *   - revise draft
 *   - ...
 *
 *   Important to break down tasks like this.
 */

#slide[
  #title[Workflows vs. agents]
  #figure(
    image("/assets/img/Screenshot 2025-12-19 at 19.57.51.png", width: 80%),
  ) <agentic>
]


#slide[
  #title[Tool calling]
  #side-by-side(gutter: 3mm, columns: (1fr, 1fr))[

    #item-by-item[
      - tool calling unlocks interaction with the external world
      - how does it work?
        - fine-tune to produce certain structured outputs
        - json strings that represent tool calls
    ]
  ][
    #figure(
      image("/assets/img/Screenshot 2025-12-21 at 17.20.22.png", height: 80%),
      numbering: none,
      caption: [
        #set text(size: 10pt)
        From 'Toolformer' paper (2022)
      ],
    )
  ]
]

#slide[
  #title[Tool calling]
  #set align(center)
  #set text(size: 0.6em)
  #v(-6em)
  #block(
    fill: luma(230),
    inset: 8pt,
    radius: 4pt,
    ```shell
    curl https://api.openai.com/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
      "model": "gpt-4.1",
      "messages": [
        {
          "role": "user",
          "content": "What is the weather like in Boston today?"
        }
      ],
      "tools": [
        {
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                  "type": "string", "enum": ["celsius", "fahrenheit"]
                }
              },
              "required": ["location"]
      ...
    }'
    ```,
  )
]


#slide[
  #title[Tool calling]
  #set align(center)
  #set text(size: 0.8em)
  #columns(2)[
    #block(
      fill: luma(230),
      inset: 8pt,
      radius: 4pt,
      ```shell
      {
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "created": 1699896916,
        "model": "gpt-4o-mini",
        "choices": [
          {
            "index": 0,
            "message": {
              "role": "assistant",
              "content": null,
              "tool_calls": [
                {
                  "id": "call_abc123",
                  "type": "function",
                  "function": {
                    "name": "get_current_weather",
                    "arguments": "{\n\"location\": \"Boston, MA\"\n}"
                  }
                }
              ]
            },
            "logprobs": null,
            "finish_reason": "tool_calls"
          }
        ],
        "usage": {
          "prompt_tokens": 82,
          "completion_tokens": 17,
          "total_tokens": 99,
          "completion_tokens_details": {
            "reasoning_tokens": 0,
            "accepted_prediction_tokens": 0,
            "rejected_prediction_tokens": 0
          }
        }
      }
      ```,
    )
  ]
]

#slide[
  #title[Exercise 2]
  #set align(horizon)
  - see `notebooks/tool-calling.py`
    - write from scratch
    - using langgraph
]

#my-new-section("Coffee break 1", "10.30")

#slide[
  #figure(image("/assets/img/coffee.jpg", height: 100%, fit: "cover"))
  #place(top + left, dx: 1cm, dy: 5cm)[
    #text("Coffee break", size: 35pt, fill: black, weight: "bold")
  ]
]


// TODO: finish this slide
// TODO: add figure
// see this https://www.ibm.com/think/topics/react-agent
#slide[
  #title[ReAct pattern]
  - design pattern for agentic systems
  - builds on Chain-of-Thought prompting + tool-use
  - simple but powerful
]


#slide[
  #title[Exercise 3]
  #set align(horizon)
  - time to build our first agent!
  - see `notebooks/ReAct.py`
    - write from scratch
    - using langgraph
  - add one new tool
]

#slide[
  #title[Advanced Concepts: self-improvement]
  - let's look at more design patterns
  - code execution
  - reflexion
  - how to evaluate?
]

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
  - donated to Linux Foundation
  - see https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
]


#slide[
  #title[Downsides of MCP]
  - letting agents write code to compose MCP much more effective
  - and much more token efficient
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

#my-new-section("Agents: Advanced Concepts", "14.00")

#imgslide(
  "Code agent",
  "/assets/img/code_agent.png",
  "Source: https://huggingface.co/blog/open-deep-research#the-gaia-benchmark",
)


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
  #title[Advanced Concepts: Memory]
  - memory allows the agent to self-improve
  - let's build a memory tool
]

#slide[
  - Exercise: deep coding agent with memory
  - use to analyze data?
  - remember what has been tried before
]

#slide[
  #title[Advanced Concepts: Evals]
  - evals: rigorous error analysis process
  - *the* factor predicting success of an Agentic AI project
]

#slide[
  #title[Advanced Concepts: Deep Agents]
  - agent with shell and code execution
]


#my-new-section("Coffee break 2", "15.00")
#my-new-section("Lab 2: MCP + advanced agents", "15.15")


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

]

// == How does it work?
//
// So there is
//
// == RLHF
//
// - instruction following
//
//
// = Retrieval Augmented Generation (RAG)
//
//
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
//
// #figure(
// image("/assets/img/gpt1_paper.png", width: 80%),
// caption: [],
// ) <gpt1>
// */
