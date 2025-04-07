# Hashing MCP Server

A Model Context Protocol (MCP) server that provides tools to calculate MD5 and SHA-256 cryptographic hashes for text data. This enables LLMs (like those in VS Code Copilot Chat, Claude, etc.) to request hash calculations.

### Available Tools

- `calculate_md5`: Calculates the MD5 hash for the provided text data.
  - Args: `text_data` (string): The string data to hash.
  - Returns: (string) The hexadecimal MD5 digest.
- `calculate_sha256`: Calculates the SHA-256 hash for the provided text data.
  - Args: `text_data` (string): The string data to hash.
  - Returns: (string) The hexadecimal SHA-256 digest.

## Setup & Installation

It's recommended to use [`uv`](https://docs.astral.sh/uv/) for managing environments and dependencies.

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <your-repo-url>
    cd hashing-mcp-server
    ```

2.  **Set Python Version (Optional but recommended):**
    Ensure you have Python 3.13 available (as specified in `.python-version`). Tools like `pyenv` can help manage Python versions.

3.  **Create Virtual Environment & Install Dependencies:**

    ```bash
    # Create and activate virtual environment
    uv venv
    source .venv/bin/activate  # Or `.\.venv\Scripts\activate` on Windows

    # Install the package and its dependencies (including dev deps)
    uv pip install -e ".[dev]"
    ```

    - `-e` installs the project in "editable" mode, linking to your source code.
    - `.[dev]` includes the development dependencies specified in `pyproject.toml`.

## Running the Server

You can run the server in several ways:

1.  **Using the installed script (Recommended):**
    (Requires the virtual environment to be active)

    ```bash
    hashing-mcp-server
    ```

2.  **Using `python -m`:**
    (Requires the virtual environment to be active)

    ```bash
    python -m hashing_mcp
    ```

3.  **Using `uv run`:**
    (Does not require activating the venv explicitly)

    ```bash
    uv run hashing-mcp-server
    ```

    Or for development (watches for changes):

    ```bash
    uv run --watch hashing-mcp-server
    ```

4.  **Using Docker (Build first):**

    ```bash
    # Build the image (from the project root)
    docker build -t hashing-mcp-server:latest .

    # Run the container interactively (for stdio)
    docker run -i --rm hashing-mcp-server:latest
    ```

## Configuration for Clients

Configure your MCP client (e.g., VS Code, Claude.app) to use this server. The key is to provide the correct command and arguments to launch the server process.

**Replace `/path/to/your/hashing-mcp-server` with the actual absolute path to the project directory.**

### VS Code (`settings.json`)

```json
"mcp.servers": {
    "hashing": {
        // Option 1: Using uv run (Recommended if uv is installed globally)
        "command": "uv",
        "args": [
            "run",
            "--python", // Optional: Specify python if needed
            "/path/to/your/python3.13",
            "--cwd", // Run from the project directory
            "/path/to/your/hashing-mcp-server",
            "hashing-mcp-server" // The script name from pyproject.toml
        ],
        // Option 2: Directly using the venv python
        // "command": "/path/to/your/hashing-mcp-server/.venv/bin/python",
        // "args": [
        //     "-m",
        //     "hashing_mcp"
        // ],
        // "options": { // Ensure it runs in the correct directory if needed
        //    "cwd": "/path/to/your/hashing-mcp-server"
        // }
        // Option 3: Using Docker
        // "command": "docker",
        // "args": [
        //    "run", "-i", "--rm", "hashing-mcp-server:latest"
        // ]
    }
}
```

### Claude Desktop (`claude-settings.json`)

```json
"mcpServers": {
  "hashing": {
    // Option 1: Using uv run (cleanest)
    "command": "uv",
    "args": [
        "run",
        "--cwd",
        "/path/to/your/hashing-mcp-server",
        "hashing-mcp-server"
     ]
    // Option 2: Using Docker
    // "command": "docker",
    // "args": ["run", "-i", "--rm", "hashing-mcp-server:latest"]
    // Option 3: Directly using venv python
    // "command": "/path/to/your/hashing-mcp-server/.venv/bin/python",
    // "args": ["-m", "hashing_mcp"],
    // "options": { "cwd": "/path/to/your/hashing-mcp-server" }
  }
}
```

## Testing the Server

1.  **Unit Tests:**
    Ensure you have installed dev dependencies (`uv pip install -e ".[dev]"`).

    ```bash
    # Activate venv if not already active
    source .venv/bin/activate

    # Run tests
    pytest
    ```

2.  **With an MCP Client:**
    After configuring your client (like VS Code), ask it questions that require hashing:

    - "Calculate the MD5 hash of the text 'hello world'"
    - "What is the SHA256 hash for the string 'MCP is cool!'?"
    - "Use the calculate_sha256 tool on this sentence: The quick brown fox jumps over the lazy dog."

    The client should recognize the request, identify the tool, potentially ask for permission, execute the tool via your server process, and display the result. Check the terminal where you ran the server (or Docker logs) for log output.

## Debugging

You can use the MCP inspector tool (`@modelcontextprotocol/inspector`) to interact with and debug the server directly.

```bash
# Ensure Node.js/npm is installed
# Install the inspector globally or use npx
npm install -g @modelcontextprotocol/inspector
# or use npx

# Run the inspector, telling it how to launch your server
# Example using uv run:
mcp-inspector uv run --cwd /path/to/your/hashing-mcp-server hashing-mcp-server

# Example using the venv python:
# mcp-inspector /path/to/your/hashing-mcp-server/.venv/bin/python -m hashing_mcp --cwd /path/to/your/hashing-mcp-server
```
