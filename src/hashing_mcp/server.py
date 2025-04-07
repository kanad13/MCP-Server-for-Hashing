# src/hashing_mcp/server.py
import hashlib
import logging
from mcp.server.fastmcp import FastMCP

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

# Initialize FastMCP server with a descriptive name
# This instance will be imported by __init__.py
mcp = FastMCP("hashing")

@mcp.tool()
async def calculate_md5(text_data: str) -> str:
    """Calculates the MD5 hash for the provided text data.

    Args:
        text_data: The string data to hash.

    Returns:
        The hexadecimal MD5 digest of the text data.
    """
    log.info(f"Received text for MD5: '{text_data[:50]}{'...' if len(text_data) > 50 else ''}'")
    try:
        # Hash functions operate on bytes, so encode the string (UTF-8 is standard)
        encoded_data = text_data.encode('utf-8')
        hasher = hashlib.md5()
        hasher.update(encoded_data)
        hex_digest = hasher.hexdigest()
        log.info(f"Calculated MD5: {hex_digest}")
        return hex_digest
    except Exception as e:
        log.error(f"Error calculating MD5: {e}", exc_info=True)
        # Re-raise or return an error message appropriate for MCP
        # For now, let FastMCP handle the exception propagation
        raise

@mcp.tool()
async def calculate_sha256(text_data: str) -> str:
    """Calculates the SHA-256 hash for the provided text data.

    Args:
        text_data: The string data to hash.

    Returns:
        The hexadecimal SHA-256 digest of the text data.
    """
    log.info(f"Received text for SHA256: '{text_data[:50]}{'...' if len(text_data) > 50 else ''}'")
    try:
        # Hash functions operate on bytes, so encode the string (UTF-8 is standard)
        encoded_data = text_data.encode('utf-8')
        hasher = hashlib.sha256()
        hasher.update(encoded_data)
        hex_digest = hasher.hexdigest()
        log.info(f"Calculated SHA256: {hex_digest}")
        return hex_digest
    except Exception as e:
        log.error(f"Error calculating SHA256: {e}", exc_info=True)
        # Re-raise or return an error message appropriate for MCP
        raise

# Note: The `if __name__ == "__main__":` block is removed.
# Server execution is now handled by `src/hashing_mcp/__init__.py`.
