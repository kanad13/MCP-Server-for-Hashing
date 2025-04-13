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

- Python 3.13 or later installed.
- A tool to manage virtual environments (like Python's built-in `venv` or `uv`).

## Installation

This section covers installing the `hashing-mcp-server` package into a virtual environment, which is necessary if you plan to run the server directly using Python. If you only plan to use Docker, you can skip this section, but you will need Docker installed.

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
uv pip install hashing-mcp-server
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
pip install hashing-mcp-server
```

_(Installation via pip/uv is now complete. The `hashing-mcp-server` command is available within the activated virtual environment.)_

## Running the Server

There are two main ways to run the `hashing-mcp-server`:

1.  **Directly using Python (via `pip` or `uv` install)**: Suitable for development or environments where Docker isn't preferred. Requires managing a Python environment (see Installation section).
2.  **Using Docker**: Recommended for easier deployment, sandboxing, and consistent environments, especially in production or shared settings.

### Option 1: Running Directly (Python Environment)

This method requires you to have installed the package in a virtual environment as described in the **Installation** section.

Before configuring your client, you can run the server directly from your terminal to ensure it starts correctly. Make sure your virtual environment is still active.

```bash
# Ensure your venv is active first! (e.g., source .venv/bin/activate)
hashing-mcp-server
```

The server will start and listen for MCP requests on standard input/output (stdio). You won't see much output unless a client connects or an error occurs. Press `Ctrl+C` to stop it. This step confirms the installation worked correctly before proceeding to client configuration.

### Option 2: Running with Docker (Recommended for Deployment)

**Prerequisites:**

- Docker installed and running on your system.
- A Dockerfile present in the root of this repository (assumed).

**1. Build the Docker Image:**

First, build the Docker image from the repository root:

```bash
# Navigate to the repository root directory if you aren't already there
# cd /path/to/MCP-Server-for-Hashing
docker build -t hashing-mcp-server .
```

- `-t hashing-mcp-server`: Tags the image with the name `hashing-mcp-server`.

**2. Run the Server in a Container (Manual Test):**

You can test if the container runs correctly:

```bash
docker run -i --rm hashing-mcp-server
```

- `-i`: Runs the container in interactive mode, keeping STDIN open so the MCP client can communicate with it.
- `--rm`: Automatically removes the container when it exits.
- `hashing-mcp-server`: The name of the image you built.

The server will start inside the container, listening on its standard input/output. Press `Ctrl+C` to stop it.

## Configuring Your MCP Client

MCP clients need to know how to start the server. Choose the configuration matching how you intend to run the server (Directly or via Docker).

**Method A: Configuring for Direct Execution (Python Environment)**

If you are running the server directly using the installed Python package, clients need the **full, absolute path** to the `hashing-mcp-server` executable _inside_ the virtual environment you created during installation.

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

**2. Copy the Full Path** displayed in the output.

**3. Update Your Client's Configuration:**

Use the copied absolute path in your specific MCP client's settings:

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

- **Other Clients:** Follow their specific instructions, providing the **full absolute path** found in step 1 as the command.

**Method B: Configuring for Docker Execution**

If you built the Docker image (`hashing-mcp-server`), configure your client to use `docker run`:

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
                  "hashing-mcp-server" // The name of the image you built
              ]
              // "env": {} // Add environment variables here if your server needed them
          }
      }
  }
  ```

- **Claude Desktop (`claude_desktop_config.json`):**

  ```json
  {
  	"mcpServers": {
  		"hashing-docker": {
  			// Use a distinct name if needed
  			"command": "docker",
  			"args": [
  				"run",
  				"-i",
  				"--rm",
  				"hashing-mcp-server" // The name of the image you built
  			]
  			// "env": {} // Add environment variables here if needed
  		}
  	}
  }
  ```

- **Other Clients (Claude Web, OpenAI Agents, etc.):**
  Adapt the `command` and `args` according to their specific configuration format, ensuring you invoke `docker run -i --rm hashing-mcp-server`. Refer to their official documentation for precise configuration steps:
  - [Claude for Desktop/Web Setup](https://modelcontextprotocol.io/quickstart/user)
  - [VSCode MCP using Copilot](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
  - [Open AI ChatGPT Agents (via Python)](https://openai.github.io/openai-agents-python/mcp/)

## Testing the Integration

Once the server package is installed (for direct execution) or the Docker image is built, and your MCP client is configured correctly for your chosen method (Direct or Docker):

1.  **Ensure the server can be launched by the client:** If you ran the server manually (either directly or via `docker run` in the terminal), make sure you stopped it (using `Ctrl+C`). The client application needs to be able to start its own instance of the server process using the command/args you provided.
2.  **Interact with your configured client:** Open your MCP client (VS Code Chat, Claude Desktop, etc.) and ask questions designed to trigger the hashing tools:
    - "Calculate the MD5 hash of the text 'hello world'"
    - "What is the SHA256 hash for the string 'MCP is cool!'?"
    - "Use the calculate_sha256 tool on this sentence: The quick brown fox jumps over the lazy dog."

The client should recognize the intent, execute the server command (either the direct path or `docker run ...`) in the background, send the request to the server process via stdio, receive the hash result, and display it back to you in the chat interface. Success means you see the correct hash output in the client.

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
    Install the package (`hashing-mcp-server`) such that changes in `src/` are reflected immediately. Also installs optional dependencies defined under `[project.optional-dependencies.dev]` in `pyproject.toml` (e.g., `pytest`, `ruff`).
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

## Packaging and Publishing

### Publishing to PyPI

_(For maintainers - Steps to release a new version)_

1.  Ensure the development venv is activated: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows).
2.  **Install build tools:** `uv pip install build twine`
3.  **Clean previous builds:** `rm -rf ./dist/*`
4.  **Build the package:** `python -m build`
5.  **Check the distribution files:** `twine check dist/*`
6.  **Upload to PyPI:** `twine upload dist/*` (Use `--repository testpypi` for testing)
7.  **Tag the release:** `git tag vX.Y.Z && git push --tags`

### Publishing to Docker Hub

_(For maintainers - Steps to release a new version)_

1.  Ensure Docker is running and you are logged in: `docker login`
2.  Push using `build_and_push.sh`

    1.  Open your terminal in that directory and run:

    ```bash
    chmod +x build_and_push.sh
    ```

    Log in to Docker Hub: Make sure you are logged in to your Docker Hub account:

    ```bash
    docker login -u <your_username>
    ```

    3. (It will prompt for your password or access token).

    4. Run the Script: Execute the script:

    ```bash
    ./build_and_push.sh
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Anthropic & Model Context Protocol Docs](https://modelcontextprotocol.io)
