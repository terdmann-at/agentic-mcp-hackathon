#import "theme.typ": *

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
  #title[Exercise 3]
  #set align(horizon)
  - see `exercises/03_tool_calling.ipynb`
    - write from scratch
    - using langgraph
]

// #my-new-section("Coffee break 1", "10.30")
#slide[
  #figure(image("/assets/img/coffee.jpg", height: 100%, fit: "cover"))
  #place(top + left, dx: 1cm, dy: 5cm)[
    #text("Coffee break", size: 35pt, fill: black, weight: "bold")
  ]
]


#include "agentic_design_patterns.typ"

#slide[
  #title[Evaluations]
  #block(inset: 2em)[
    #item-by-item[
      - evals: rigorous error analysis process
      - *the* factor predicting success of an Agentic AI project
      - requires a shift of mind set
      - deterministic vs. Probabilistic //: Traditional engineering focuses on removing ambiguity (`Input A + Code B = Output C`), whereas agents require managing probability and "reasoning". // Illustration: Instead of being a Traffic Controller who owns the roads and lights, you must become a Dispatcher giving instructions to a driver (the LLM) who might take a shortcut or get lost.
      - testing vs. evals //: Transitioning from binary unit tests to evaluation frameworks that measure semantic accuracy and "trajectories."Illustration: Success is no longer an exact string match; it's whether the agent successfully achieved the user's intent over a 20-turn conversation.
      - errors as inputs:
        - errors are valuable feedback used to help the agent recover and pivot // Illustration: If step 4 of a 5-minute task fails, don't crash the program; catch the error and feed it back to the agent so it can try a different approach.
    ]
  ]
]

