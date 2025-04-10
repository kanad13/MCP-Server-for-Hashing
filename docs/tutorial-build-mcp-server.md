# Build your own MCP Hashing server

- **On this page**
- This page shows how to build the MCP Hashing server and connect it to a client of your choice.
  - **Supported Hosts:**
  - [VS Code](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
  - [Claude for Desktop](https://modelcontextprotocol.io/introduction)
  - [Open AI ChatGPT](https://openai.github.io/openai-agents-python/mcp/)
- **What we will be building**
  - A simple server that calculates the MD5 and SHA256 hashes of a string.
  - The server will be built using the MCP framework.
  - It will expose two tools: `calculate_md5` and `calculate_sha256`.
- **Important Note**
  - This tutorial focuses on creating a basic, single-file MCP server (`my_hashing_server.py`) for quick experimentation, similar to the official [MCP quick start guide](https://modelcontextprotocol.io/quickstart/server).
  - For a more structured, package-ready example (using `src/` layout, build tools, etc.), please refer to the main code and main README in this repository.

## Setup environment

- **Install uv**
  - uv is a command line tool that helps you create and manage virtual environments.
  - It is a wrapper around the built-in `venv` module.
  - It is similar to `virtualenv`, but it is more lightweight and easier to use.
  - Installation instructions [here](https://docs.astral.sh/uv/getting-started/installation/)
- **Setup Hashing project**
  - Follow these steps in your terminal:

```bash
# Create a new directory for our project
uv init hashing_mcp
cd hashing_mcp

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]"

# Create our server file
touch my_hashing_server.py
```

## Build MCP Server

- Open `my_hashing_server.py` and add the following code:

```python
import hashlib
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with a descriptive name
mcp = FastMCP("hashing")

@mcp.tool()
async def calculate_md5(text_data: str) -> str:
    """Calculates the MD5 hash for the provided text data.

    Args:
        text_data: The string data to hash.

    Returns:
        The hexadecimal MD5 digest of the text data.
    """
    # Hash functions operate on bytes, so encode the string (UTF-8 is standard)
    encoded_data = text_data.encode('utf-8')
    hasher = hashlib.md5()
    hasher.update(encoded_data)
    hex_digest = hasher.hexdigest()
    print(f"Received text for MD5: '{text_data[:50]}...'") # Optional: log input
    print(f"Calculated MD5: {hex_digest}")             # Optional: log output
    return hex_digest

@mcp.tool()
async def calculate_sha256(text_data: str) -> str:
    """Calculates the SHA-256 hash for the provided text data.

    Args:
        text_data: The string data to hash.

    Returns:
        The hexadecimal SHA-256 digest of the text data.
    """
    # Hash functions operate on bytes, so encode the string (UTF-8 is standard)
    encoded_data = text_data.encode('utf-8')
    hasher = hashlib.sha256()
    hasher.update(encoded_data)
    hex_digest = hasher.hexdigest()
    print(f"Received text for SHA256: '{text_data[:50]}...'") # Optional: log input
    print(f"Calculated SHA256: {hex_digest}")           # Optional: log output
    return hex_digest

if __name__ == "__main__":
    print("Starting Hashing MCP Server...")
    # Initialize and run the server using stdio transport for desktop clients
    mcp.run(transport='stdio')
    print("Hashing MCP Server stopped.")
```

## Configure MCP Server

- **MCP follows a client-server architecture**
  - `MCP clients (like VS Code)` connect to MCP servers and request actions on behalf of the AI model
  - `MCP servers` provide one or more tools that expose specific functionalities through a well-defined interface
  - The `Model Context Protocol (MCP)` defines the message format for communication between clients and servers, including tool discovery, invocation, and response handling
- **What we will do now**
  - Previous steps created a server that can calculate the MD5 and SHA256 hashes of a string.
  - Now we will configure a client to connect to this server and use it.
  - We will use VS Code as our client as described [here](https://code.visualstudio.com/docs/copilot/chat/mcp-servers).
  - To follow the same instructions for Claude for Desktop, see [here](https://modelcontextprotocol.io/quickstart/user).
- **Configure MCP Server in VS Code**
  - Open your settings.json for vscode workspace or user, and add this entry:

```json
"mcp": {
		"servers": {
			"hashing-tutorial": {
				"command": "uv",
				"args": [
					"--directory",
					"/actual-path-to-your-folder/hashing_mcp",
					"run",
					"my_hashing_server.py"
				]
			}
		}
	}
```

## Test MCP Server

- **Ask questions like**
  - "Calculate the MD5 hash of the text 'hello world'"
  - "What is the SHA256 hash for the string 'MCP is cool!'?"
  - "Use the calculate_sha256 tool on this sentence: The quick brown fox jumps over the lazy dog."
- **Expected behavior**
  - VSCode should
    - recognize the request,
    - identify the appropriate tool (`calculate_md5` or `calculate_sha256`),
    - ask for your permission to run it,
    - execute the tool via your local `hashing_utility.py` script, and
    - return the hexadecimal hash result.

## (Optional) Next Steps: Packaging Your Server

- While this tutorial created a single runnable script (`my_hashing_server.py`), real-world tools are often distributed as installable Python packages. This makes them easier to share and manage.
- If you wanted to turn this simple server into a package, you would typically:
  - **Restructure:** Move the code into a proper package structure (e.g., `src/my_package_name/server.py`).
  - **Create `pyproject.toml`:** Define package metadata (name, version, dependencies) and build system details. Crucially, you'd define an entry point script.
  - **Define Script Entry Point:** Add a section like this to `pyproject.toml`:

```toml
[project.scripts]
my-hashing-server-command = "my_package_name.cli:main"
```

- This requires creating a `cli.py` file with a `main` function that runs `mcp.run()`.
- **Build & Install:** Use tools like `uv` or `pip` with `build` to create distributable files (wheels) and install the package into a virtual environment.
- **Update Client Config:** The client configuration (e.g., VS Code `settings.json`) would then use the _installed script command_ (e.g., `/path/to/venv/bin/my-hashing-server-command`) instead of `uv run ...`.
- **For a complete example of a packaged MCP server, examine the structure and `pyproject.toml` file in the root of this repository, which builds the `hashing-mcp` package.**
