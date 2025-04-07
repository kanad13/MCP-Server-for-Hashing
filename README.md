# Hashing MCP Server Package

A straightforward [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server providing tools to calculate MD5 and SHA-256 cryptographic hashes for text data. It's designed for easy integration with MCP clients like VS Code Copilot Chat, Claude for Desktop, or other LLM interfaces supporting the protocol.

This package exposes two primary tools:

- `calculate_md5`: Calculates the MD5 hash of a given string.
- `calculate_sha256`: Calculates the SHA-256 hash of a given string.

## Features

- Calculates MD5 hashes for text input.
- Calculates SHA-256 hashes for text input.
- Runs as an MCP server using `stdio` transport, ideal for desktop clients.
- Installable as a Python package via PyPI.
- Provides a simple command-line entry point (`hashing-mcp-server`) to start the server.

## Installation

Ensure you have Python 3.10 or later installed.

You can use `uv` (recommended) or standard `pip` for installation.

**Using `uv`:**

```bash
# Create a new directory (optional, but good practice)
mkdir hashing_mcp_setup && cd hashing_mcp_setup

# Initialize uv project (optional)
# uv init

# Create virtual environment and activate it
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install the package
uv pip install hashing-mcp
```

**Using `pip`:**

```bash
# Create a new directory (optional, but good practice)
mkdir hashing_mcp_setup && cd hashing_mcp_setup

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

Once installed and your virtual environment is activated, start the MCP server from your terminal:

```bash
hashing-mcp-server
```

This command starts the server, which listens for MCP requests via standard input/output. You typically won't interact with this terminal directly; your MCP client connects to it based on its configuration. Press `Ctrl+C` to stop the server.

## Configuring MCP Clients

Configure your MCP client to use the installed server. The essential part is telling the client the exact command (including the full path) to run the `hashing-mcp-server` executable.

**Supported Hosts (Examples):**

- [VS Code Copilot Chat](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Claude for Desktop](https://modelcontextprotocol.io/quickstart/user)
- [Open AI ChatGPT Agents (via Python)](https://openai.github.io/openai-agents-python/mcp/)

**Finding the Executable Path:**

After activating your virtual environment, find the absolute path to the script:

- On Linux/macOS: `which hashing-mcp-server`
- On Windows: `where hashing-mcp-server`

Copy the full path output by these commands.

**Example: VS Code (`settings.json`)**

_Important:_ Replace `/path/to/your/virtualenv/bin/hashing-mcp-server` with the **actual absolute path** you found using `which` or `where`.

```json
// settings.json
"mcp": {
    "servers": {
        // You can name this server key anything, e.g., "hasher" or "cryptoTools"
        "hashing": {
            // Use the full path to the executable within your virtual environment
            "command": "/path/to/your/virtualenv/bin/hashing-mcp-server"
        }
    }
}
```

**Example: Claude for Desktop**

Follow the setup instructions provided by the Claude for Desktop application or the MCP documentation (like the [User Quickstart](https://modelcontextprotocol.io/quickstart/user)), providing the full path to the `hashing-mcp-server` executable when prompted.

### Testing the Integration

Once configured, try asking your MCP client questions that should trigger the tools:

- "Calculate the MD5 hash of the text 'hello world'"
- "What is the SHA256 hash for the string 'MCP is cool!'?"
- "Use the calculate_sha256 tool on this sentence: The quick brown fox jumps over the lazy dog."

The client should recognize the request, potentially ask for permission to use the tool, execute the command via the `hashing-mcp-server`, and display the calculated hash.

## Development Setup

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

3.  **Install in editable mode:**
    Install the package such that changes in your source code are immediately reflected without reinstalling.

    ```bash
    # Install in editable mode AND include optional development dependencies
    # (like pytest, ruff, mypy) defined in pyproject.toml under [project.optional-dependencies.dev]
    uv pip install -e ".[dev]"

    # OR, if you don't have/need specific dev dependencies defined yet:
    # uv pip install -e .
    ```

4.  **Run the server during development:**
    You can run the server using the installed script (because of `-e`):
    ```bash
    hashing-mcp-server
    ```
    Or execute the module directly:
    ```bash
    python -m hashing_mcp.cli
    ```

## Packaging and Publishing to PyPI

_(For maintainers)_ Steps to release a new version:

1.  **Install build tools:**
    Ensure you have `build` and `twine` installed in your environment.

    ```bash
    uv pip install build twine
    ```

2.  **Clean previous builds (optional but recommended):**

    ```bash
    rm -rf dist/ build/ *.egg-info
    ```

3.  **Build the package:**
    This command creates the source distribution (`.tar.gz`) and wheel (`.whl`) in the `dist/` directory.

    ```bash
    python -m build
    ```

4.  **Check the distribution files:**
    `twine check` verifies that the package metadata and built files are valid.

    ```bash
    twine check dist/*
    ```

5.  **Upload to PyPI:**
    This command uploads your package to the Python Package Index. You'll need a PyPI account and API token configured.

    ```bash
    twine upload dist/*
    ```

    _(Use `twine upload --repository testpypi dist/_` to upload to the TestPyPI repository first for testing)\*

6.  **Test the published package:**
    Install the newly published package in a fresh virtual environment to ensure it works correctly.
    ```bash
    # In a new directory/environment
    uv venv test_env
    source test_env/bin/activate
    uv pip install hashing-mcp
    hashing-mcp-server # Test running the server
    # Deactivate when done: deactivate
    ```
