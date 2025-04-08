# Understanding Model Context Protocol (MCP) and Agentic AI

You've likely been hearing more about "Model Context Protocol" lately. But what does it really mean?

In this document, I'll break down the concept of Model Context Protocol (MCP) and its significance in the realm of Agentic AI.

## Why is Context Important?

Large Language Models (LLMs) don't "think" or "remember" in the human sense.

Their ability to generate good responses depends entirely on the **context** provided.

![](../assets/mcp-50.png)

## What Constitutes "Context"?

Context is defined as `any information that can help an LLM generate a better response.`

![](../assets/mcp-51.png)

## Why is Context Standardization Important?

Context standardization improves the quality of LLM responses by ensuring that the information provided is relevant, accurate, and structured in a way that the model can effectively utilize.

![](../assets/mcp-52.png)

## What is MCP?

- **Definition**
  - The Model Context Protocol (MCP) refers to a specific `set of rules, conventions, and formats designed to standardize how applications structure and provide context information to LLMs.`
  - It is one of the first open protocols for LLMs, aiming to create a common language for context exchange.
- **Goal**
  - Think of MCP like a USB-C port for AI applications.
  - Just as USB-C provides a standardized way to connect your devices to various peripherals and accessories, MCP provides a standardized way to connect AI models to different data sources and tools.
- **Focus**
  - MCP places a strong emphasis on standardizing access to dynamic, external data sources (files, databases, APIs) required for grounding LLM responses (e.g., for Retrieval-Augmented Generation - RAG).
  - MCP also aims to simplify the integration process for developers, making it easier to build applications that leverage LLM capabilities.

![](../assets/mcp-53.png)

## How does MCP correlate with Agentic AI?

- **Agentic AI**
  - Refers to AI systems that can perform tasks autonomously, make decisions, and interact with the external world.
  - It is a step beyond traditional LLMs, which primarily generate text based on input prompts.
  - To know more about Agentic AI, check out my previous blog post [Agentic AI Demo](https://www.kunal-pathak.com/blog/agentic-ai/){:target="\_blank" rel="noopener noreferrer"}.
- **Evolution of Agentic AI**
  - The evolution of Agentic AI can be divided into three stages:
    1. **Stage 1: LLMs without Agency**
       - LLMs generate text based on input prompts but cannot perform actions or interact with the external world.
    2. **Stage 2: LLMs with Limited Agency**
       - LLMs can call specific tool APIs to perform tasks but require custom code for each integration.
    3. **Stage 3: LLMs with Full Agency (MCP)**
       - LLMs can interact with multiple tools and data sources through a standardized protocol (MCP), making them more robust and easier to integrate.

![](../assets/mcp-11.png)

- **Stage 01 Capabilities**
  - Generates coherent text, code, etc.
  - Can perform reasoning tasks based on its internal knowledge.
- **Stage 01 Limitation**
  - Cannot Act.
  - Operates purely on internal knowledge and cannot interact with or affect the external world (e.g., browse live websites, query databases, send messages).
  - It can generate code to do these things, but cannot execute it.

![](../assets/mcp-12.png)

- **Improvement over Stage 01**
  - LLM gains agency.
  - It can now interact with the external world by directly calling specific tool APIs based on custom-built integration code.
  - Enables more complex, real-world tasks.
- **Key Challenge in Stage 02**
  - Brittleness & High Maintenance.
  - Integrations are tightly coupled to individual tool APIs.
  - Each tool requires custom code within the LLM application.
  - Any change to a tool's API (new parameters, endpoint changes) breaks the integration and requires developers to update the LLM application code.
  - This is difficult to scale and error-prone.

![](../assets/mcp-13.png)

- **Improvement over Stage 2**
  - Introduces a standardized interface (MCP) acting as a middle layer.
  - The LLM application communicates with tools using a single, consistent protocol (MCP), rather than diverse, direct API calls.
- **Benefit of Stage 03**
  - Decoupling & Robustness.
  - The LLM application is decoupled from the specific tool APIs. If a tool's API changes, only its dedicated MCP adapter (server) needs updating (often handled by the tool provider).
  - The LLM application (client) remains unchanged.
  - This makes integrations robust, scalable, and significantly easier to build and maintain.

## MCP Architecture

Diagram below shows the architecture of the Model Context Protocol (MCP).

![](../assets/mcp-21.png)

- **Components of the MCP architecture**
  - `MCP Hosts`
    - These are the applications that need to provide context to an LLM.
    - Examples include IDEs (like VS Code extensions), desktop applications (like Claude Desktop), etc.
  - `MCP Clients`
    - Reside within the Host application and manage communication using the MCP protocol.
    - They connect to one or more MCP Servers to request context data.
  - `MCP Servers`
    - Specialized programs designed to expose specific data sources via the standardized MCP protocol.
    - Each server handles a particular type of data (e.g., file system access, API interactions, etc.)
    - They maintain a 1:1 connection with a client requesting data.
  - `Local Data Sources`
    - Files, databases, or services residing on the user's local machine.
    - MCP Servers securely access and provide data from these sources.
  - `Remote Services`
    - External systems, APIs, or services available over the network/internet.
    - MCP Servers connect and retrieve data from these services via the MCP protocol.
- **Benefit of this architecture**
  - This architecture allows a Host application to query multiple specialized Servers to assemble the necessary context from diverse sources before potentially sending it to an LLM.

## Standardized Tool Access

**MCP is a Client-Server Protocol for Standardized Tool Access.**

It enables seamless communication between applications and data sources, ensuring that tools can be accessed in a consistent manner.

![](../assets/mcp-31.png)

## MCP client-server interaction

This section shows how the MCP client-server interaction works.

![](../assets/mcp-41.png)

## Source Drawing for Images

All images on this page are drawn by me and the original source is available on [Excalidraw](https://excalidraw.com/#json=XwQTmDqlGg6c4C6lT4XDG,X6EfWy4VBggzevh43rDymw){:target="\_blank" rel="noopener noreferrer"}.

## Acknowledgements

- [Anthropic](https://modelcontextprotocol.io){:target="\_blank" rel="noopener noreferrer"}
- [Ras Mic on Youtube](https://www.youtube.com/watch?v=uWZ-Yqj8nhw){:target="\_blank" rel="noopener noreferrer"}
