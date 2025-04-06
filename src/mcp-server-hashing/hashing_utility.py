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
