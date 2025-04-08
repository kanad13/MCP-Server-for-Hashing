import pytest
import pytest_asyncio  # Required for async tests if not using pytest >= 7.0 implicitly

# Import the functions to test from your server module
from hashing_mcp.server import calculate_md5, calculate_sha256

# --- Test Data ---
# Define some test cases with known inputs and expected outputs
# You can generate expected hashes using online tools or Python's hashlib for verification
test_cases = [
    (
        "hello world",
        "5eb63bbbe01eeed093cb22bb8f5acdc3",  # Expected MD5
        "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",  # Expected SHA256
    ),
    (
        "",  # Test empty string
        "d41d8cd98f00b204e9800998ecf8427e",  # Expected MD5
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",  # Expected SHA256
    ),
]

# --- Test Functions ---

# Use pytest.mark.parametrize to run the same test logic with different inputs
@pytest.mark.parametrize("input_text, expected_md5, _", test_cases)
@pytest.mark.asyncio # Mark the test as asynchronous
async def test_calculate_md5(input_text, expected_md5, _):
    """Tests the calculate_md5 tool function."""
    result = await calculate_md5(text_data=input_text)
    assert result == expected_md5

@pytest.mark.parametrize("input_text, _, expected_sha256", test_cases)
@pytest.mark.asyncio # Mark the test as asynchronous
async def test_calculate_sha256(input_text, _, expected_sha256):
    """Tests the calculate_sha256 tool function."""
    result = await calculate_sha256(text_data=input_text)
    assert result == expected_sha256
