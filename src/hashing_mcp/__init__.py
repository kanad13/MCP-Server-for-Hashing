# src/hashing_mcp/__init__.py
import asyncio
import argparse
from .server import mcp # Import the initialized FastMCP instance

def main():
    """MCP Hashing Server - MD5 and SHA256 hashing tools for MCP"""
    parser = argparse.ArgumentParser(
        description="Provides MD5 and SHA256 hashing capabilities via MCP."
    )
    # Add any future arguments here if needed
    # parser.add_argument("--some-option", type=str, help="An example option")
    args = parser.parse_args()

    print("Starting Hashing MCP Server...")
    try:
        # FastMCP's run method is synchronous and manages its own loop
        # for stdio transport. No explicit asyncio.run needed here.
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        print("\nHashing MCP Server stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Hashing MCP Server shut down.")

if __name__ == "__main__":
    # This allows running the module directory directly in some cases,
    # but the primary entry points are the script or `python -m`.
    main()
