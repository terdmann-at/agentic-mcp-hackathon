#import "theme.typ": *


#slide[
  #title[How does text-generation with LLMs work?]
  #set align(center + horizon)
  #only(1)[#grid(
      // columns: (auto, auto, auto, auto, auto, auto),
      columns: (1fr, 1fr, 1fr, 0.2fr, 1fr, 0.2fr, 1fr),
      align: center + horizon,
      row-gutter: 3em,
      column-gutter: 50pt,
    )[Prompt][Model][Vocabulary][ ][Probabilities][ ][Sample][
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
      #stack(spacing: 1em, dir: ttb, sym.arrow, hide[sym.arrow], hide[sym.arrow], hide[sym.arrow], hide[sym.arrow])
    ][
      #stack(spacing: 1em, dir: ttb, text(weight: "bold")[talk], hide[green], hide[chair], hide[but], hide[...])
    ]
  ]
  #only(2)[#grid(
      // columns: (auto, auto, auto, auto, auto, auto, auto),
      columns: (1fr, 1fr, 1fr, 0.2fr, 1fr, 0.2fr, 1fr),
      align: center + horizon,
      row-gutter: 3em,
      column-gutter: 50pt,
    )[Prompt][Model][Vocabulary][ ][Probabilities][ ][Sample][
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
      #stack(spacing: 1em, dir: ttb, hide[sym.arrow], sym.arrow, hide[sym.arrow], hide[sym.arrow], hide[sym.arrow])
    ][
      #stack(
        spacing: 1em,
        dir: ttb,
        hide()[choice],
        text(weight: "bold")[about],
        hide()[especially],
        hide()[cellar],
        hide()[...],
      )
    ]
  ]
]

#slide[
  #title[How does text-generation with LLMs work?]
  #set align(horizon)
  #block(inset: 2em)[
    #item-by-item[
      - given some words $w_1, w_2, ..., w_t$, LLMs predict the probability of the next word $w_(t+1)$
      - LLMs are a model of: $ P_theta (w_(t+1) | w_1, w_2, ..., w_t) $
      - the model weights $theta$ are pre-trained on huge amounts of text
      - and then trained some more (post-training) to follow instructions
      - the words $w_1, ...$ are the "prompt" and allow us to use the model
    ]
  ]
]



#slide[
  #title[What is so great about LLMs?]
  #set align(horizon)
  #block(inset: 2em)[
    #item-by-item[
      - In-Context Learning
      - instead of training a model on a dataset, we just write instructions
      - the model can learn from examples in the prompt
      - 0-shot performance / reasoning
      - Why does it work?
      - large datasets
      - attention mechanism
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
  #title[Reinforcement Learning from Human Feedback (RLHF)]
  #figure(image("/assets/img/RLHF_diagram.svg", height: 80%, fit: "contain"), numbering: none, caption: [
    #set text(size: 10pt)
    Note: when do you use RL? if you don't know the loss function yourself (works with thumbs-up/thumbs-down)
  ])
]

#slide[
  #title[Reasoning Models: CoT]
  #figure(
    image("../assets/img/CoT-prompting.jpg", height: 80%, fit: "contain"),
    numbering: none,
    caption: [
      #set text(size: 10pt)
      An example of classic CoT prompting from the 2022 Large Language Models are Zero-Shot Reasoners paper (https://arxiv.org/abs/2205.11916).
    ],
  )
]

#imgslide(
  "Reasoning Models",
  "../assets/img/reasoning-1.png",
  "Source: https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-reasoning-llms",
)

#imgslide(
  "Reasoning Models",
  "../assets/img/reasoning-2.png",
  "Source: https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-reasoning-llms",
)

#imgslide(
  "Reasoning Models",
  "../assets/img/reasoning-3.png",
  "Source: https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-reasoning-llms",
)

#imgslide(
  "Reasoning Models",
  "../assets/img/reasoning-4.png",
  "Source: https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-reasoning-llms",
)

#imgslide(
  "Reasoning Models",
  "../assets/img/reasoning-5.png",
  "Source: https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-reasoning-llms",
)

#imgslide(
  "Reasoning Models: beam search with PRM",
  "../assets/img/reasoning-6.png",
  "Source: https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-reasoning-llms",
)


#slide[
  #title[Reasoning Models: 4 ways to improve reasoning]
  #block(inset: 0.2em)[
    #item-by-item[
      1. inference-time scaling: increasing computational resources during inference
        - Chain of thought prompting is one version of that
        - Another one is best of N: Generating multiple solutions and using a process-based verifier reward model (it has to be separately trained) to select the best response. Such a model learns how effective reasoning should look like
      2. Pure reinforcement learning (RL)
        - DeepSeek-R1-Zero was trained exclusively with RL and discovered that reasoning emerges as a behavior from that
          - The accuracy reward uses the LeetCode compiler to verify coding answers and a deterministic system to evaluate mathematical responses.
          - The format reward relies on an LLM judge to ensure responses follow the expected format, such as placing reasoning steps inside <think> tags.
    ]
  ]
]

#slide[
  #title[Reasoning Models: 4 ways to improve reasoning]
  #block(inset: 0.2em)[
    #item-by-item[
      3. Supervised finetuning and reinforcement learning (SFT + RL)
        - multiple rounds of instruction based fine-tuning (similar to RLHF) and RL with accuracy rewards
        - datasets of CoT data are generated and used for fine-tuning
      4. Pure supervised finetuning (SFT) and distillation
        - train smaller models on output of larger models
    ]
  ]
]


#slide[
  #title[Mixture of Experts (MoE)]
  #one-by-one[
    - in regular LLMs (e.g. GPT-3), every parameter is used to process every single token
  ][
    - MoE: break up network into sub-networks ("experts") and train a gating network
  ][
    - the gating network learns to route tokens to different networks
  ][
    - mathematically this is a weighted combination, but the actual implementations select Top-K, leading
    to just K sub-networks being used for the processing
  ][
    - allows to train much larger models, since at any time, only a smaller part gets activated
  ]

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
  #block(inset: 1em)[
    - we can call the OpenAI API to get a completion
    - how to we have a conversation?
    #block(inset: 1em)[
      ```python
      model = ChatOpenAI()
      messages = []
      while True:
        user_input = input("User: ")
        messages.append(("user", user_input))
        response = model.invoke(messages)
        messages.append(("assistant", response.content))
        print(f"AI: {response.content}")
      ```
    ]
  ]
]

#show raw.where(block: true): block.with(fill: luma(240), inset: 1em, radius: 0.5em, width: 100%)

#slide[
  #title[Building Chatbots: LangGraph]
  #block(inset: (x: 3em, y: 0em))[
    #set text(size: 15pt)
    ```python
    from langchain_openai import ChatOpenAI
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.graph import START, MessagesState, StateGraph
    model = ChatOpenAI()
    graph = (
      StateGraph(MessagesState)
      .add_node(
        "chatbot",
        lambda state: {"messages": model.invoke(state["messages"])}
      )
      .add_edge(START, "chatbot")
      .compile(checkpointer=MemorySaver())
    )
    config = {"configurable": {"thread_id": "1"}}
    while True:
      user_input = input("User: ")
      response = graph.invoke({"messages": [("user", user_input)]}, config)
      print(f"AI: {response['messages'][-1].content}")
    ```
  ]
]

#slide[
  #title[Building Chatbots: LangGraph (functional)]
  #block(inset: (x: 3em, y: 0em))[
    #set text(size: 15pt)
    ```python
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.func import entrypoint

    @entrypoint(checkpointer=MemorySaver())
    def chat_workflow(new_message: str, previous: list = None):
        history = previous or []
        history.append(("user", new_message))
        response = model.invoke(history)
        history.append(("assistant", response.content))
        return history

    config = {"configurable": {"thread_id": "1"}}
    while True:
        user_input = input("User: ")
        output = chat_workflow.invoke(user_input, config=config)
        print("AI: ", output[-1][1])

    ```
  ]
]


#slide[
  #title[Exercise 1]
  #block(inset: (x: 3em, y: 1em))[
    - see `exercises/01_chatbot.ipynb`
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
    - see `exercises/02_rag.ipynb`
  ]
]



