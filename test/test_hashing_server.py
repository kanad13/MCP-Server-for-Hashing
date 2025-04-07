# test/test_hashing_server.py
import pytest
import asyncio

# Import the functions directly for testing
# Note: We are testing the functions, not the full MCP server loop here
from hashing_mcp.server import calculate_md5, calculate_sha256

# Known hash values for "hello world"
HELLO_WORLD_MD5 = "5eb63bbbe01eeed093cb22bb8f5acdc3"
HELLO_WORLD_SHA256 = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"

# Known hash values for an empty string
EMPTY_MD5 = "d41d8cd98f00b204e9800998ecf8427e"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

@pytest.mark.asyncio
async def test_calculate_md5_hello_world():
    """Test MD5 calculation for 'hello world'."""
    result = await calculate_md5("hello world")
    assert result == HELLO_WORLD_MD5

@pytest.mark.asyncio
async def test_calculate_sha256_hello_world():
    """Test SHA256 calculation for 'hello world'."""
    result = await calculate_sha256("hello world")
    assert result == HELLO_WORLD_SHA256

@pytest.mark.asyncio
async def test_calculate_md5_empty_string():
    """Test MD5 calculation for an empty string."""
    result = await calculate_md5("")
    assert result == EMPTY_MD5

@pytest.mark.asyncio
async def test_calculate_sha256_empty_string():
    """Test SHA256 calculation for an empty string."""
    result = await calculate_sha256("")
    assert result == EMPTY_SHA256

@pytest.mark.asyncio
async def test_calculate_md5_unicode():
    """Test MD5 calculation with Unicode characters."""
    text = "你好世界" # "Hello World" in Chinese
    expected_md5 = "65396ee4aad0b4f17aacd1c6112ee364"
    result = await calculate_md5(text)
    assert result == expected_md5

@pytest.mark.asyncio
async def test_calculate_sha256_unicode():
    """Test SHA256 calculation with Unicode characters."""
    text = "你好世界" # "Hello World" in Chinese
    expected_sha256 = "beca6335b20ff57ccc47403ef4d9e0b8fccb4442b3151c2e7d50050673d43172"
    result = await calculate_sha256(text)
    assert result == expected_sha256

# To run tests:
# 1. Ensure pytest and pytest-asyncio are installed (`uv pip install pytest pytest-asyncio`)
# 2. Run `pytest` in the project root directory.
