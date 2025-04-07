# Hashing MCP Server Package

An MCP Server offering tools to calculate MD5 and SHA-256 cryptographic hashes for text data, designed for use with LLMs and other MCP clients.

## What is this?

This package provides a simple [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes two tools:

- `calculate_md5`: Calculates the MD5 hash of a given string.
- `calculate_sha256`: Calculates the SHA-256 hash of a given string.

It's designed to be easily integrated with MCP clients like VS Code Copilot Chat, Claude for Desktop, or others supporting the protocol.

## Features

- Calculates MD5 hashes.
- Calculates SHA-256 hashes.
- Runs as an MCP server using `stdio` transport, suitable for desktop clients.
- Installable as a Python package.
- Provides a simple command-line entry point (`hashing-mcp-server`) to start the server.

## Installation

You can install this package using pip (or your preferred Python package manager like `uv`):

```bash
pip install hashing-mcp # Or pip install . if installing from local source
# Or using uv:
# uv pip install hashing-mcp
```

- Ensure you have Python 3.10 or newer installed.

## Usage

Once installed, you can start the MCP server from your terminal:

```bash
hashing-mcp-server
```

This will start the server, listening for MCP requests via standard input/output. You typically don't interact with this directly; your MCP client will connect to it based on your configuration. Press `Ctrl+C` to stop the server.

## Configuring MCP Clients

Configure your MCP client to use the installed server. The key is to tell the client how to run the `hashing-mcp-server` command.

**Supported Hosts:**

- [VS Code Copilot Chat](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Claude for Desktop](https://modelcontextprotocol.io/introduction)
- [Open AI ChatGPT Agents](https://openai.github.io/openai-agents-python/mcp/)

**Example: VS Code (`settings.json`)**

_Important:_ Replace `/path/to/your/virtualenv/bin/hashing-mcp-server` with the _actual_ path where the `hashing-mcp-server` script was installed by pip/uv in your environment. You can find this using `which hashing-mcp-server` (Linux/macOS) or `where hashing-mcp-server` (Windows) in your activated virtual environment.

```json
// settings.json
"mcp": {
    "servers": {
        "hashing": {
            "command": "/path/to/your/virtualenv/bin/hashing-mcp-server",
        }
    }
}
```

**Example: Claude for Desktop**

Follow the instructions [here](https://modelcontextprotocol.io/quickstart/user), providing the path to the `hashing-mcp-server` executable when prompted.

### Testing with a Client

Once configured, ask your client questions like:

- "Calculate the MD5 hash of the text 'hello world'"
- "What is the SHA256 hash for the string 'MCP is cool!'?"
- "Use the calculate_sha256 tool on this sentence: The quick brown fox jumps over the lazy dog."

The client should identify the tool, potentially ask for permission, execute the command, and return the result from the server.

## Development Setup

If you want to contribute or modify the code:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/kanad13/MCP-Server-for-Hashing.git
    cd MCP-Server-for-Hashing
    ```

2.  **Set up environment (using uv):**

    ```bash
    # Optional: Ensure you're using the correct Python version (uses .python-version)
    # pyenv install $(cat .python-version)
    # pyenv local $(cat .python-version)

    # Create and activate virtual environment
    uv venv
    source .venv/bin/activate # or .venv\Scripts\activate on Windows
    ```

3.  **Install in editable mode with development dependencies:**

    ```bash
    uv pip install -e ".[dev]" # Assuming you add a [project.optional-dependencies] group
    # Or just install editable if no dev deps yet:
    # uv pip install -e .
    ```

    Editable mode (`-e`) links the installed package to your source code, so changes are reflected immediately without reinstalling.

4.  **Run the server during development:**
    You can still use the installed script:
    ```bash
    hashing-mcp-server
    ```
    Or run the module directly:
    ```bash
    python -m hashing_mcp.cli
    ```

## Package and push to PyPi

- Install Twine inside your virtual environment:

```bash
uv pip install twine
```

- Check Distribution Files

```bash
twine check dist/*
```

- Push the package to PyPi:

```bash
twine upload dist/*
```

- Test the package in a fresh virtual environment:

```bash
uv pip install hashing-mcp
hashing-mcp-server
```
