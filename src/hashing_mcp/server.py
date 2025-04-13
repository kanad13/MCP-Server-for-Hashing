import hashlib
import logging
from mcp.server.fastmcp import FastMCP

# Configure basic logging to capture informational messages and errors.
# This helps in monitoring the server's operation and diagnosing issues.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---

# Define a maximum input length to prevent potential Denial-of-Service (DoS) attacks.
# Very large inputs could consume excessive resources during hashing.
# See: https://modelcontextprotocol.io/docs/concepts/transports#security-considerations
MAX_INPUT_LENGTH = 1_000_000  # Max characters allowed in input strings

# Initialize the FastMCP server. The name "hashing" identifies this service.
# This 'mcp' instance will expose the tools defined below.
mcp = FastMCP("hashing")

# --- Tool Definitions ---

@mcp.tool()
async def calculate_md5(text_data: str) -> str:
    """Calculates the MD5 hash for the provided text data.

    MD5 is a widely used cryptographic hash function producing a 128-bit hash value.
    Note: MD5 is considered cryptographically broken for collision resistance and should not be used for security-critical applications like password hashing.
    It can still be useful for checksums or non-security-related purposes.

    Args:
        text_data: The string data to hash.

    Returns:
        The hexadecimal representation of the MD5 digest.

    Raises:
        ValueError: If the input `text_data` exceeds `MAX_INPUT_LENGTH`.
        RuntimeError: For unexpected internal errors during the hashing process.
    """
    # Input validation: Reject excessively long inputs to prevent resource exhaustion.
    if len(text_data) > MAX_INPUT_LENGTH:
        error_message = f"Input data exceeds maximum allowed length of {MAX_INPUT_LENGTH} characters."
        logger.warning(f"MD5 calculation rejected: {error_message} (Input length: {len(text_data)})")
        raise ValueError(error_message) # Inform client about invalid input.

    try:
        # Hash functions require byte input, so encode the string using UTF-8.
        encoded_data = text_data.encode('utf-8')

        # Perform the MD5 hashing.
        hasher = hashlib.md5()
        hasher.update(encoded_data)
        hex_digest = hasher.hexdigest()

        # Log successful operation for monitoring. Truncate input in logs for brevity.
        logger.info(f"Calculated MD5 for input (truncated): '{text_data[:80]}...' -> {hex_digest}")
        return hex_digest
    except ValueError as ve:
        # Handle potential specific errors (e.g., encoding issues, though unlikely here).
        logger.error(f"ValueError during MD5 calculation: {ve}", exc_info=False)
        # Re-raise the specific error if it's meaningful for the client.
        raise
    except Exception as e:
        # Catch-all for unexpected errors during hashing.
        # Log the full error details internally for debugging.
        logger.error(f"Unexpected error calculating MD5: {e}", exc_info=True)
        # Raise a generic error to the client to avoid leaking internal implementation details.
        # This enhances security by not exposing potentially sensitive information in stack traces.
        raise RuntimeError("An internal error occurred during MD5 calculation.")


@mcp.tool()
async def calculate_sha256(text_data: str) -> str:
    """Calculates the SHA-256 hash for the provided text data.

    SHA-256 is part of the SHA-2 family of cryptographic hash functions, producing a 256-bit hash value. It is widely considered secure for various applications, including digital signatures and data integrity checks.

    Args:
        text_data: The string data to hash.

    Returns:
        The hexadecimal representation of the SHA-256 digest.

    Raises:
        ValueError: If the input `text_data` exceeds `MAX_INPUT_LENGTH`.
        RuntimeError: For unexpected internal errors during the hashing process.
    """
    # Input validation: Reject excessively long inputs to prevent resource exhaustion.
    if len(text_data) > MAX_INPUT_LENGTH:
        error_message = f"Input data exceeds maximum allowed length of {MAX_INPUT_LENGTH} characters."
        logger.warning(f"SHA256 calculation rejected: {error_message} (Input length: {len(text_data)})")
        raise ValueError(error_message) # Inform client about invalid input.

    try:
        # Hash functions require byte input, so encode the string using UTF-8.
        encoded_data = text_data.encode('utf-8')

        # Perform the SHA-256 hashing.
        hasher = hashlib.sha256()
        hasher.update(encoded_data)
        hex_digest = hasher.hexdigest()

        # Log successful operation for monitoring. Truncate input in logs for brevity.
        logger.info(f"Calculated SHA256 for input (truncated): '{text_data[:80]}...' -> {hex_digest}")
        return hex_digest
    except ValueError as ve:
        # Handle potential specific errors (e.g., encoding issues).
        logger.error(f"ValueError during SHA256 calculation: {ve}", exc_info=False)
        # Re-raise the specific error if it's meaningful for the client.
        raise
    except Exception as e:
        # Catch-all for unexpected errors during hashing.
        # Log the full error details internally for debugging.
        logger.error(f"Unexpected error calculating SHA256: {e}", exc_info=True)
        # Raise a generic error to the client to avoid leaking internal implementation details.
        raise RuntimeError("An internal error occurred during SHA256 calculation.")
