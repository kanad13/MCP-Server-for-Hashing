# MCP Server for cryptographic hashing

A Model Context Protocol (MCP) server for MD5 and SHA-256 hashing. This server enables LLMs to process cryptographic requests efficiently.

## Available Tools

The server offers 2 tools:

- `calculate_md5`: Computes the MD5 hash of a given text.
- `calculate_sha256`: Computes the SHA-256 hash of a given text.

The server is designed to be used with MCP clients like VS Code Copilot Chat, Claude for Desktop, and other LLM interfaces that support the [Model Context Protocol](https://modelcontextprotocol.io).

## Understand MCP and Build Your Own MCP Server

If you are new to the concept of Model Context Protocol (MCP), then you can use these resources:

- **What is MCP?**
  - [Understanding Model Context Protocol & Agentic AI](https://www.kunal-pathak.com/blog/model-context-protocol/)
- **How can I build my own MCP Server?**
  - [Simple tutorial on how to build your own MCP Server](https://github.com/kanad13/MCP-Server-for-Hashing/blob/master/docs/tutorial-build-mcp-server.md)
- **Where to find the `hashing-mcp` server package?**
  - You can find the [Python Package on PyPI](https://pypi.org/project/hashing-mcp/)
  - You can find the source code in this [GitHub repository](https://github.com/kanad13/MCP-Server-for-Hashing)
  - See the sections below for installation and usage instructions.

## Server in action

The gif below shows how the MCP server processes requests and returns the corresponding cryptographic hashes.
I have used Claude Desktop as an example, but it works equally well with other MCP clients like VSCode.
![MCP Server in action](/assets/mcp-60.gif)

## Prerequisites

- Python 3.10 or later installed.
- A tool to manage virtual environments (like Python's built-in `venv` or `uv`).

## Installation

This section covers installing the `hashing-mcp` package into a virtual environment.

**(Choose one method: `uv` or `pip`)**

**1. Using `uv` (Recommended):**

```bash
# Create a new directory (optional, but good practice)
mkdir my_mcp_setup && cd my_mcp_setup

# Create virtual environment and activate it
uv venv
# Activate on Linux/macOS:
source .venv/bin/activate
# Activate on Windows (Command Prompt/PowerShell):
# .venv\Scripts\activate
# (Ensure you are in the 'my_mcp_setup' directory when activating)

# Install the package
uv pip install hashing-mcp
```

**2. Using `pip`:**

```bash
# Create a new directory (optional, but good practice)
mkdir my_mcp_setup && cd my_mcp_setup

# Create virtual environment
python -m venv .venv

# Activate it
# Activate on Linux/macOS:
source .venv/bin/activate
# Activate on Windows (Command Prompt/PowerShell):
# .venv\Scripts\activate
# (Ensure you are in the 'my_mcp_setup' directory when activating)

# Install the package
pip install hashing-mcp
```

_(Installation is now complete. The `hashing-mcp-server` command is available within the activated virtual environment.)_

## Running the Server Manually (Optional Verification)

Before configuring your client, you can run the server directly from your terminal to ensure it starts correctly. Make sure your virtual environment is still active.

```bash
# Ensure your venv is active first! (e.g., source .venv/bin/activate)
hashing-mcp-server
```

The server will start and listen for MCP requests on standard input/output (stdio). You won't see much output unless a client connects or an error occurs. Press `Ctrl+C` to stop it. This step confirms the installation worked correctly before proceeding to client configuration.

## Configuring Your MCP Client

MCP clients need to know the exact command to execute the `hashing-mcp-server`. Since the client application (like VS Code or Claude Desktop) likely won't run with your specific virtual environment automatically activated, you **must** provide the **full, absolute path** to the `hashing-mcp-server` executable _inside_ the virtual environment you created during installation.

**1. Find the Absolute Path:**

With your virtual environment still active (run `source .venv/bin/activate` or `.venv\Scripts\activate` again if needed), use the appropriate command for your operating system in the terminal:

```bash
# On Linux/macOS:
which hashing-mcp-server
# Example Output: /home/user/my_mcp_setup/.venv/bin/hashing-mcp-server

# On Windows (Command Prompt/PowerShell):
where hashing-mcp-server
# Example Output: C:\Users\User\my_mcp_setup\.venv\Scripts\hashing-mcp-server.exe
```

**2. Copy the Full Path** displayed in the output from the command above.

**3. Update Your Client's Configuration:**

Use the copied absolute path in your specific MCP client's settings. Here are some common examples:

- **VS Code (`settings.json`):**

  ```json
  // In your VS Code settings.json (User or Workspace)
  "mcp": {
      "servers": {
          // You can name this key anything, e.g., "hasher" or "cryptoTools"
          "hashing": {
              // Paste the full, absolute path you copied here:
              "command": "/path/to/your/virtualenv/bin/hashing-mcp-server"
              // No 'args' needed when running the installed script directly
          }
      }
  }
  ```

  _(Replace `/path/to/your/virtualenv/bin/hashing-mcp-server` with your actual path)_

- **Claude Desktop (`claude_desktop_config.json`):**

  ```json
  {
  	"mcpServers": {
  		"hashing": {
  			// Paste the full, absolute path you copied here:
  			"command": "/path/to/your/virtualenv/bin/hashing-mcp-server"
  			// Adjust the path based on your actual installation location.
  		}
  	}
  }
  ```

- **Other Clients (Claude Web, OpenAI Agents, etc.):**
  Follow the specific instructions provided by your client application. When prompted for the command or path to the MCP server executable, provide the **full absolute path** you found in step 1. Refer to their official documentation for precise configuration steps:
  - [Claude for Desktop/Web Setup](https://modelcontextprotocol.io/quickstart/user)
  - [VSCode MCP using Copilot](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
  - [Open AI ChatGPT Agents (via Python)](https://openai.github.io/openai-agents-python/mcp/)

## Testing the Integration

Once the server package is installed and your MCP client is configured with the correct absolute path:

1.  **Ensure the server can be launched by the client:** If you ran the server manually in the previous verification step, make sure you stopped it (using `Ctrl+C` in its terminal). The client application needs to be able to start its own instance of the server process using the command path you provided.
2.  **Interact with your configured client:** Open your MCP client (VS Code Chat, Claude Desktop, etc.) and ask questions designed to trigger the hashing tools:
    - "Calculate the MD5 hash of the text 'hello world'"
    - "What is the SHA256 hash for the string 'MCP is cool!'?"
    - "Use the calculate_sha256 tool on this sentence: The quick brown fox jumps over the lazy dog."

The client should recognize the intent, execute the `hashing-mcp-server` command in the background using the absolute path you provided, send the request to the server process via stdio, receive the hash result, and display it back to you in the chat interface. Success means you see the correct hash output in the client.

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
    # Activate on Linux/macOS:
    source .venv/bin/activate
    # Activate on Windows:
    # .venv\Scripts\activate
    ```
3.  **Install in editable mode with development dependencies:**
    Install the package such that changes in `src/` are reflected immediately. Also installs optional dependencies defined under `[project.optional-dependencies.dev]` in `pyproject.toml` (e.g., `pytest`, `ruff`).
    ```bash
    uv pip install -e ".[dev]"
    ```
4.  **Run the server during development:**
    Ensure your virtual environment is active. You can run the server using the installed script (available due to the `-e` flag):
    ```bash
    hashing-mcp-server
    ```
    Or execute the module directly:
    ```bash
    python -m hashing_mcp.cli
    ```

## Packaging and Publishing to PyPI

_(For maintainers - Steps to release a new version)_

1.  Ensure the development venv is activated: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows).
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
