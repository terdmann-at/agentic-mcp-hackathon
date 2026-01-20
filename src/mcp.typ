
#import "theme.typ": *


#my-new-section("MCP", "13.00")


#slide[
  #title[Model Context Protocol (MCP)]
  #block(inset: 2em)[
    #item-by-item[
      One year of MCP:
      - first released Nov 24
      - supports tools, resources and prompts
        - exetuble actions (API calls, running scripts)
        - local files, db queries, cloud documents etc.
        - structured prompts
      - recently donated to Linux Foundation: https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
    ]
  ]
]


#slide[
  #title[Why use MCP?]
  #block(inset: 2em)[
    #item-by-item[
      - interoperability: solves the NxM problem
      - reusing toolsets across different agents with slightly different APIs
      - not required for tool calling: list of available tools it provided to LLM with every request
    ]
  ]
]


#slide[
  #title[Downsides of MCP]
  #block(inset: 2em)[
    #item-by-item[
      - slower than calling a tool locally (needs network request etc)
      - letting agents write code to compose MCP much more effective
      - and much more token efficient
      - MCP offers no way for servers to declare their runtime/dependency needs
      - Since tools are drawn from arbitrary sources, they are not aware of what other tools are available to the agent. Their instructions can't account for the rest of the toolbox
      - Agents tend to be less effective at tool use as the number of tools grows
    ]
  ]
]


// TODO: fill this in
#slide[
  #title[Exercise 5]
  #block(inset: 2em)[
    #item-by-item[
      - see `exercises/05_mcp.ipynb`
        - write MCP server
        - connect to MCP server
    ]
  ]
]

