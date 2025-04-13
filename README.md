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
- **Where to find the `hashing-mcp-server` package?**
  - You can find the [Python Package on PyPI](https://pypi.org/project/hashing-mcp-server/)
  - You can find the source code in this [GitHub repository](https://github.com/kanad13/MCP-Server-for-Hashing)
  - See the sections below for installation and usage instructions.

## Server in action

The gif below shows how the MCP server processes requests and returns the corresponding cryptographic hashes.
I have used Claude Desktop as an example, but it works equally well with other MCP clients like VSCode.
![MCP Server in action](/assets/mcp-60.gif)

## Prerequisites

- **To Run via Docker:** Docker installed and running.
- **To Run Directly:** Python 3.13+ and a virtual environment tool (`venv`, `uv`).
- **To Contribute/Develop:** Git, Python 3.13+, `uv` (recommended) or `pip`, Docker (optional, for testing build).

## Option 1: Running the Server with Docker (Recommended)

This is the simplest way to run the server without managing Python environments directly.

**1. Get the Docker Image:**

- **Pull from Docker Hub (Easiest):**

  ```bash
  docker pull kunalpathak13/hashing-mcp-server:latest
  ```

**2. Configure Your MCP Client:**

Configure your client to use `docker run`.

- **VS Code (`settings.json`):**

  ```json
  // In your VS Code settings.json (User or Workspace)
  "mcp": {
      "servers": {
          "hashing-docker": { // Use a distinct name if needed
              "command": "docker",
              "args": [
                  "run",
                  "-i",      // Keep STDIN open for communication
                  "--rm",    // Clean up container after exit
                  "kunalpathak13/hashing-mcp-server:latest" // Change the tag to your version if needed e.g. "hashing-mcp-server:X.Y.Z"
              ]
          }
      }
  }
  ```

- **Claude Desktop (`claude_desktop_config.json`):**

  ```json
  {
  	"mcpServers": {
  		"hashing-docker": {
  			"command": "docker",
  			"args": [
  				"run",
  				"-i",
  				"--rm",
  				"kunalpathak13/hashing-mcp-server:latest" // Change the tag to your version if needed e.g. "hashing-mcp-server:X.Y.Z"
  			]
  		}
  	}
  }
  ```

- **Other Clients:** Adapt according to their docs, using `docker` as the command and `run -i --rm IMAGE_NAME` as arguments. Refer to their official documentation for precise configuration steps:

  - [Claude for Desktop/Web Setup](https://modelcontextprotocol.io/quickstart/user)
  - [VSCode MCP using Copilot](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
  - [Open AI ChatGPT Agents (via Python)](https://openai.github.io/openai-agents-python/mcp/)

**3. Test the Integration:**

Once configured, interact with your MCP client (VS Code Chat, Claude Desktop, etc.). Ask questions designed to trigger the hashing tools:

- "Calculate the MD5 hash of the text 'hello world'"
- "What is the SHA256 hash for the string 'MCP is cool!'?"

The client should start the Docker container in the background using the command you provided, send the request, receive the hash result, and display it.

## Option 2: Running the Server Directly (Python Environment)

Use this method if you prefer not to use Docker or for development purposes.

**1. Set Up Environment & Install:**

```bash
# Create a dedicated directory and navigate into it
mkdir my_mcp_setup && cd my_mcp_setup

# --- Create & Activate Virtual Environment (Choose ONE method) ---
# Method A: Using uv (Recommended):
uv venv
source .venv/bin/activate # Linux/macOS
# .venv\Scripts\activate # Windows

# Method B: Using standard venv:
# python -m venv .venv
# source .venv/bin/activate # Linux/macOS
# .venv\Scripts\activate # Windows
# ---

# --- Install the package (within the active venv, choose ONE method) ---
# Method A: Using uv:
uv pip install hashing-mcp-server

# Method B: Using pip:
# pip install hashing-mcp-server
# ---
```

**2. Find the Executable Path:**

With the virtual environment _active_, find the full, absolute path to the installed script:

```bash
# On Linux/macOS:
which hashing-mcp-server
# Example Output: /home/user/my_mcp_setup/.venv/bin/hashing-mcp-server

# On Windows (Command Prompt/PowerShell):
where hashing-mcp-server
# Example Output: C:\Users\User\my_mcp_setup\.venv\Scripts\hashing-mcp-server.exe
```

**Copy the full path** displayed in the output.

**3. Configure Your MCP Client:**

Use the **absolute path** you copied in the client configuration.

- **VS Code (`settings.json`):**

  ```json
  // In your VS Code settings.json (User or Workspace)
  "mcp": {
      "servers": {
          // You can name this key anything, e.g., "hasher" or "cryptoTools"
          "hashing": {
              // Paste the full, absolute path you copied here:
              "command": "/full/path/to/your/virtualenv/bin/hashing-mcp-server"
              // No 'args' needed when running the installed script directly
          }
      }
  }
  ```

  _(Replace the example path with your actual path)_

- **Claude Desktop (`claude_desktop_config.json`):**

  ```json
  {
  	"mcpServers": {
  		"hashing": {
  			// Paste the full, absolute path you copied here:
  			"command": "/full/path/to/your/virtualenv/bin/hashing-mcp-server"
  		}
  	}
  }
  ```

  _(Replace the example path with your actual path)_

- **Other Clients:** Follow their specific instructions, providing the **full absolute path** found in step 2 as the command.

**4. Test the Integration:**

Once configured, interact with your MCP client (VS Code Chat, Claude Desktop, etc.). Ask questions designed to trigger the hashing tools: - "Use the calculate_md5 tool on 'hello world'." - "Compute the SHA256 hash for the text 'MCP rocks'."

The client should start the server script using the absolute path you provided, send the request, receive the hash result, and display it.

## Contributing / Development Setup

Follow these steps if you want to modify the server code or contribute.

**1. Clone the Repository:**

```bash
git clone https://github.com/kanad13/MCP-Server-for-Hashing.git
cd MCP-Server-for-Hashing
```

**2. Set Up Development Environment:**

```bash
# Create & Activate Virtual Environment (using uv recommended)
uv venv
source .venv/bin/activate # Linux/macOS
# .venv\Scripts\activate # Windows

# Install in editable mode with development dependencies
uv pip install -e ".[dev]"
```

_(This installs the package such that code changes in `src/` take effect immediately without reinstalling. It also installs tools defined in `[project.optional-dependencies.dev]` like `pytest`)_

**3. Running Locally During Development:**
Ensure your development virtual environment is active. You can run the server using:

```bash
# Run the installed script (available due to -e flag)
hashing-mcp-server
```

Or execute the module directly:

```bash
python -m hashing_mcp.cli
```

*(You might temporarily configure your MCP client to point to the executable path within *this* specific development `.venv` for integrated testing)*

**4. Running Tests:**
Ensure your development virtual environment is active:

```bash
pytest
```

## Maintainer Tasks: Releasing a New Version

_(For project maintainers)_

The release process (building, testing, tagging, pushing to PyPI and Docker Hub) is automated by the `build_and_push.sh` script located in the repository root.

**Prerequisites for Running the Script:**

- You must be inside the **activated development virtual environment** (`source .venv/bin/activate` or `.venv\Scripts\activate`).
- Required tools must be available: `uv` (or `pip`), `twine`, `git`, `docker`.
- Credentials must be configured:
  - Docker: Logged in via `docker login`.
  - PyPI: Production API token configured via `TWINE_USERNAME=__token__` and `TWINE_PASSWORD=pypi-...` environment variables or `~/.pypirc`.
- Push access granted to the target Git repository (`origin` by default) and the Docker Hub repository (`kunalpathak13/hashing-mcp-server` by default).

**Release Steps:**

1.  Ensure the `version` field in `pyproject.toml` is updated to the correct new version number.
2.  Commit and push any final code changes to the main branch.
3.  Make the release script executable (one-time setup): `chmod +x build_and_push.sh`
4.  Activate the virtual environment: `source .venv/bin/activate` (or equivalent).
5.  Run the script from the repository root: `./build_and_push.sh`
6.  The script will perform all steps: build, check, upload to PyPI, build Docker image, tag Docker image (version and `latest`), push Docker images, create Git tag, push Git tag.
7.  Verify the new package version is live on PyPI and the new Docker tags are available on Docker Hub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Anthropic & Model Context Protocol Docs](https://modelcontextprotocol.io)
