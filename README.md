# MCP Server for cryptographic hashing

A Model Context Protocol (MCP) server for MD5 and SHA-256 hashing. This server enables LLMs to process cryptographic requests efficiently.

## Available Tools

The server offers 2 tools:

- `calculate_md5`: Computes the MD5 hash of a given text.
- `calculate_sha256`: Computes the SHA-256 hash of a given text.

The server is designed to be used with MCP clients like VS Code Copilot Chat, Claude for Desktop, and other LLM interfaces that support the [Model Context Protocol](https://modelcontextprotocol.io).

## Code Overview

[This Github repository serves two main purposes](https://github.com/kanad13/MCP-Server-for-Hashing):

1.  **Provides a ready-to-use `hashing-mcp` server package:** You can install this package directly to add hashing capabilities to your MCP-enabled application. See **Installation** and **Usage** sections below.
2.  **Acts as an educational resource:** It includes detailed guides to help you understand MCP concepts and learn how this specific server was built. See the **Learning More** section below.

## Understanding Model Context Protocol

Check out these resources for understanding and building MCP servers:

- **What is MCP?**
  - [Understanding Model Context Protocol & Agentic AI](https://github.com/kanad13/MCP-Server-for-Hashing/blob/master/docs/understanding-mcp.md)
- **How can I build my own MCP Server?**
  - [Simple tutorial on how to build your own MCP Server](https://github.com/kanad13/MCP-Server-for-Hashing/blob/master/docs/tutorial-build-mcp-server.md)
    _(Note: This guide walks through creating the package structure found in this repository.)_

## Server in action

The gif below shows how the MCP server processes requests and returns the corresponding cryptographic hashes.
I have used VSCode as an example, but it works equally well with other MCP clients like Claude for Desktop.
![MCP Server in action](/assets/mcp-54.gif)

## Installation

Ensure you have Python 3.10 or later installed. I recommend using a virtual environment.

**Using `uv` (Recommended):**

```bash
# Create a new directory (optional, but good practice)
mkdir my_mcp_setup && cd my_mcp_setup

# Create virtual environment and activate it
uv venv
source .venv/bin/activate  # On Linux/macOS
# .venv\Scripts\activate    # On Windows

# Install the package
uv pip install hashing-mcp
```

**Using `pip`:**

```bash
# Create a new directory (optional, but good practice)
mkdir my_mcp_setup && cd my_mcp_setup

# Create virtual environment
python -m venv .venv

# Activate it
# Linux/macOS:
source .venv/bin/activate
# Windows (Command Prompt/PowerShell):
# .venv\Scripts\activate

# Install the package
pip install hashing-mcp
```

## Usage

Once the package is installed and your virtual environment is activated, you can start the MCP server.

**1. Run the Server:**

Open your terminal and run:

```bash
hashing-mcp-server
```

This command starts the server, which will listen for MCP requests via standard input/output (stdio). You typically won't interact with this terminal directly after starting it; your MCP client will communicate with it in the background. Press `Ctrl+C` to stop the server.

**2. Configure Your MCP Client:**

Configure your MCP client (e.g., VS Code, Claude Desktop) to use the installed `hashing-mcp-server`. The key is to tell the client the **exact command** needed to run the server script.

- **Find the Executable Path:** After activating your virtual environment, find the absolute path to the installed script:

  - On Linux/macOS: `which hashing-mcp-server`
  - On Windows: `where hashing-mcp-server`
  - Copy the full path output by the command.

- **Example: VS Code (`settings.json`)**

  _**Important:** Replace `/path/to/your/virtualenv/bin/hashing-mcp-server` with the **actual absolute path** you found above._

  ```json
  // In your VS Code settings.json (User or Workspace)
  "mcp": {
      "servers": {
          // You can name this key anything, e.g., "hasher" or "cryptoTools"
          "hashing": {
              // Use the full, absolute path to the executable within your virtual environment
              "command": "/path/to/your/virtualenv/bin/hashing-mcp-server"
              // No 'args' needed when running the installed script directly
          }
      }
  }
  ```

- **Example: Other Clients (Claude, OpenAI Agents, etc.)**

  Follow the specific instructions for your client application. When asked for the command or path to the MCP server, provide the **full absolute path** to the `hashing-mcp-server` executable you found earlier. Refer to their documentation:

  - [Claude for Desktop](https://modelcontextprotocol.io/quickstart/user)
  - [Open AI ChatGPT Agents (via Python)](https://openai.github.io/openai-agents-python/mcp/)

**3. Test the Integration:**

Once configured, ask your MCP client questions that should trigger the tools:

- "Calculate the MD5 hash of the text 'hello world'"
- "What is the SHA256 hash for the string 'MCP is cool!'?"
- "Use the calculate_sha256 tool on this sentence: The quick brown fox jumps over the lazy dog."

The client should identify the request, invoke the `hashing-mcp-server` via the configured command, and display the calculated hash result.

## Development (Contributing)

If you want to modify or contribute to this package:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/kanad13/MCP-Server-for-Hashing.git
    cd MCP-Server-for-Hashing
    ```
2.  **Set up the development environment (using uv):**
    ```bash
    # Create and activate virtual environment
    uv venv
    source .venv/bin/activate # or .venv\Scripts\activate on Windows
    ```
3.  **Install in editable mode with development dependencies:**
    Install the package such that changes in `src/` are reflected immediately. Also installs optional dependencies defined under `[project.optional-dependencies.dev]` in `pyproject.toml` (e.g., `pytest`, `ruff`).
    ```bash
    uv pip install -e ".[dev]"
    ```
4.  **Run the server during development:**
    You can run the server using the script (available due to `-e`):
    ```bash
    hashing-mcp-server
    ```
    Or execute the module directly:
    ```bash
    python -m hashing_mcp.cli
    ```

## Packaging and Publishing to PyPI

_(For maintainers - Steps to release a new version)_

1.  Ensure that venv is activated: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows).
2.  **Install build tools:** `uv pip install build twine`
3.  **Clean previous builds:** `rm -rf ./dist/*`
4.  **Build the package:** `python -m build`
5.  **Check the distribution files:** `twine check dist/*`
6.  **Upload to PyPI:** `twine upload dist/*` (Use `--repository testpypi` for testing)
7.  **Tag the release:** `git tag vX.Y.Z && git push --tags`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Anthropic & Model Context Protocol Docs](https://modelcontextprotocol.io)
