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
touch hashing_utility.py
```

## Build MCP Server

- Open `hashing_utility.py` and add the following code:

```python
# hashing_utility.py (inside src/hashing_mcp/)

import hashlib
from mcp.server.fastmcp import FastMCP
import logging # Consider using standard logging

# Setup basic logging (optional but good practice)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastMCP server with a descriptive name
mcp = FastMCP("hashing")

@mcp.tool()
async def calculate_md5(text_data: str) -> str:
    # ... (your existing function code) ...
    encoded_data = text_data.encode('utf-8')
    hasher = hashlib.md5()
    hasher.update(encoded_data)
    hex_digest = hasher.hexdigest()
    # Use logging instead of print for libraries
    logging.info(f"Received text for MD5: '{text_data[:50]}...'")
    logging.info(f"Calculated MD5: {hex_digest}")
    return hex_digest

@mcp.tool()
async def calculate_sha256(text_data: str) -> str:
    # ... (your existing function code) ...
    encoded_data = text_data.encode('utf-8')
    hasher = hashlib.sha256()
    hasher.update(encoded_data)
    hex_digest = hasher.hexdigest()
    logging.info(f"Received text for SHA256: '{text_data[:50]}...'")
    logging.info(f"Calculated SHA256: {hex_digest}")
    return hex_digest

# ---- NEW FUNCTION for entry point ----
def run_server():
    """Starts the Hashing MCP Server."""
    logging.info("Starting Hashing MCP Server...")
    # Initialize and run the server using stdio transport for desktop clients
    # You might want to allow configuration of transport via args/env vars later
    try:
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        logging.info("Server stopped by user.")
    finally:
        logging.info("Hashing MCP Server shut down.")
# --------------------------------------

# Keep this block for direct execution during development if desired
if __name__ == "__main__":
    run_server()
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
			"hashing": {
				"command": "uv",
				"args": [
					"--directory",
					"/actual-path-to-your-folder/mcp-server-for-hashing/src/mcp-server-hashing",
					"run",
					"hashing_utility.py"
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
