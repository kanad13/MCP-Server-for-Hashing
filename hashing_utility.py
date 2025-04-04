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
