# src/hashing_mcp/cli.py

import logging
from .server import mcp # Import the mcp instance from server.py within the same package

logger = logging.getLogger(__name__)

def main():
    """
    Entry point function for the command-line script defined in pyproject.toml.
    Initializes and runs the MCP server.
    """
    print("Starting Hashing MCP Server (via hashing-mcp-server command)...")
    logger.info("Initializing Hashing MCP Server...")
    try:
        # Initialize and run the server using stdio transport for desktop clients
        # Ensure mcp instance is ready (it's initialized in server.py)
        mcp.run(transport='stdio')
    except Exception as e:
        logger.critical(f"Hashing MCP Server failed to run: {e}", exc_info=True)
        print(f"Error: Hashing MCP Server failed to run: {e}")
    finally:
        logger.info("Hashing MCP Server stopped.")
        print("Hashing MCP Server stopped.")

if __name__ == "__main__":
    # This allows running the CLI script directly for testing:
    # python -m hashing_mcp.cli
    main()
