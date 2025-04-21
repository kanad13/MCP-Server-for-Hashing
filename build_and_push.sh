#!/bin/bash

# ==============================================================================
# Combined Build, Package, Tag, and Push Script for hashing-mcp-server
# ==============================================================================
#
# PURPOSE:
#   Automates the full release process for the hashing-mcp-server project:
#   1. Python packaging: Builds sdist/wheel, checks, and uploads to PRODUCTION PyPI.
#   2. Docker image: Builds, tags (version & latest), and pushes to Docker Hub.
#   3. Git tagging: Creates and pushes a version tag to the remote Git repository.
#
# !!! IMPORTANT PREREQUISITE !!!
#   This script MUST be run from WITHIN the activated development virtual environment for the project. Activate it first:
#
#   # On Linux/macOS:
#   source .venv/bin/activate
#   # On Windows (Command Prompt/PowerShell):
#   # .venv\Scripts\activate
#
# OTHER PREREQUISITES:
# - `bash`, `grep`, `cut`, `rm` must be available.
# - `uv` must be installed *within the activated venv* (or replace `uv pip` with `pip`).
# - `python` (the one from the venv) must be available.
# - `docker` must be installed, running, and logged into Docker Hub (`docker login`).
# - `twine` credentials MUST be configured for PRODUCTION PyPI, typically via:
#   - Environment variables: `TWINE_USERNAME=__token__` and `TWINE_PASSWORD=pypi-api-token...`
#   - Or a correctly configured `~/.pypirc` file.
# - `git` must be installed and configured with push access to the remote 'origin' repository (e.g., via SSH keys or HTTPS credentials).
# - A `pyproject.toml` file must exist in the current directory with a `version = "X.Y.Z"` line.
# - A `Dockerfile` must exist in the current directory.
# - The script should be run from the root directory of the repository.
#
# USAGE:
# 1. Activate the virtual environment: `source .venv/bin/activate`
# 2. Ensure all other prerequisites are met (logins, tokens, etc.).
# 3. Make the script executable (if needed): `chmod +x release.sh`
# 4. Run the script: `./release.sh`
#
# ==============================================================================

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Your Docker Hub username / organization
DOCKER_HUB_USER="kunalpathak13"
# Base name for the Docker image (without user/org prefix)
IMAGE_BASE_NAME="hashing-mcp-server"
# Full Docker image name
IMAGE_NAME="${DOCKER_HUB_USER}/${IMAGE_BASE_NAME}"
# Git remote name to push tags to
GIT_REMOTE_NAME="origin"

echo "=================================================="
echo "🚀 Starting Full Release Process..."
echo "   (Ensure you activated the venv first!)"
echo "=================================================="

# --- 1. Get Version from pyproject.toml ---
echo "🔍 Extracting version from pyproject.toml..."
VERSION=$(grep '^version *=' pyproject.toml | cut -d '"' -f 2)

# Check if VERSION was successfully extracted
if [ -z "$VERSION" ]; then
  echo "❌ Error: Could not automatically determine version from pyproject.toml." >&2
  echo "   Ensure the file exists and contains a line like 'version = \"1.7.0\"'" >&2
  exit 1
fi

echo "✅ Version found: ${VERSION}"
echo "--------------------------------------------------"

# --- 2. Check if running inside a virtual environment ---
# A simple check - might not be foolproof on all systems/shells
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️ WARNING: \$VIRTUAL_ENV is not set. Are you sure you activated the virtual environment?"
    echo "   Continuing, but Python packaging steps might fail or use system packages."
    # Optionally, you could make this an error:
    # echo "❌ Error: Script must be run inside an activated virtual environment." >&2
    # exit 1
fi

# --- 3. Install/Verify Python Build Tools ---
echo "🐍 Ensuring Python build tools (build, twine) are installed using uv..."
# Installs/updates tools within the active venv. Use 'pip install' if uv not preferred/available.
uv pip install --quiet build twine
echo "✅ Build tools checked/installed."
echo "--------------------------------------------------"

# --- 4. Clean Previous Python Builds ---
echo "🧹 Cleaning previous Python build artifacts (dist/)..."
rm -rf ./dist/*
echo "✅ Clean complete."
echo "--------------------------------------------------"

# --- 5. Build Python Package ---
echo "📦 Building Python package (sdist and wheel)..."
# Uses the python from the activated venv
python -m build
echo "✅ Package build complete."
echo "--------------------------------------------------"

# --- 6. Check Python Distribution Files ---
echo "🧐 Checking distribution files using twine..."
twine check dist/*
echo "✅ Distribution files check passed."
echo "--------------------------------------------------"

# --- 7. Upload Python Package to PRODUCTION PyPI ---
echo "☁️ Uploading package to PRODUCTION PyPI..."
echo "   (Ensure TWINE_USERNAME and TWINE_PASSWORD env vars are set for PyPI API token)"
# No --repository flag means it uploads to the default (production PyPI)
twine upload dist/*
echo "✅ Package uploaded to Production PyPI."
echo "--------------------------------------------------"

# --- 8. Build Docker Image ---
echo "🐳 Building Docker image: ${IMAGE_NAME}:${VERSION}..."
docker build -t "${IMAGE_NAME}:${VERSION}" .
echo "✅ Docker build complete."
echo "--------------------------------------------------"

# --- 9. Tag Docker Image ---
echo "🏷️ Tagging ${IMAGE_NAME}:${VERSION} as ${IMAGE_NAME}:latest..."
docker tag "${IMAGE_NAME}:${VERSION}" "${IMAGE_NAME}:latest"
echo "✅ Docker tagging complete."
echo "--------------------------------------------------"

# --- 10. Push Docker Image to Docker Hub ---
echo " Pushing Docker tag: ${IMAGE_NAME}:${VERSION}..."
echo "   (Ensure you are logged into Docker Hub: 'docker login')"
docker push "${IMAGE_NAME}:${VERSION}"
echo "✅ Version tag push complete."
echo "--------------------------------------------------"

echo " Pushing Docker tag: ${IMAGE_NAME}:latest..."
docker push "${IMAGE_NAME}:latest"
echo "✅ Latest tag push complete."
echo "--------------------------------------------------"

# --- 11. Create Git Tag ---
GIT_TAG="v${VERSION}"
echo "️ Creating Git tag: ${GIT_TAG}..."
# Check if tag already exists locally
if git rev-parse "${GIT_TAG}" >/dev/null 2>&1; then
  echo "⚠️ Warning: Git tag ${GIT_TAG} already exists locally. Skipping creation."
else
  git tag "${GIT_TAG}"
  echo "✅ Git tag ${GIT_TAG} created locally."
fi
echo "--------------------------------------------------"

# --- 12. Push Git Tag ---
echo " Pushing Git tag ${GIT_TAG} to remote '${GIT_REMOTE_NAME}'..."
echo "   (Ensure you have push access to the remote repository)"
# Check if tag already exists remotely before pushing
if git ls-remote --tags "${GIT_REMOTE_NAME}" | grep -q "refs/tags/${GIT_TAG}"; then
    echo "️ Warning: Git tag ${GIT_TAG} already exists on the remote '${GIT_REMOTE_NAME}'. Skipping push."
else
    git push "${GIT_REMOTE_NAME}" "${GIT_TAG}"
    echo "✅ Git tag ${GIT_TAG} pushed to ${GIT_REMOTE_NAME}."
fi
echo "--------------------------------------------------"


echo "=================================================="
echo "✅✅✅ Full Release Process Completed Successfully! ✅✅✅"
echo "=================================================="
echo "Summary:"
echo "  - Python Package Version: ${VERSION}"
echo "    - Built: dist/"
echo "    - Pushed to Production PyPI"
echo "  - Docker Image: ${IMAGE_NAME}"
echo "    - Built image tagged: ${VERSION}, latest"
echo "    - Pushed tags to Docker Hub: ${VERSION}, latest"
echo "  - Git Tag: ${GIT_TAG}"
echo "    - Created/verified tag: ${GIT_TAG}"
echo "    - Pushed/verified tag to remote '${GIT_REMOTE_NAME}'"
echo "--------------------------------------------------"
echo "Consumers can now:"
echo "  - Install Python package: pip install hashing-mcp-server==${VERSION}"
echo "  - Pull latest Docker image: docker pull ${IMAGE_NAME}"
echo "  - Pull specific Docker image: docker pull ${IMAGE_NAME}:${VERSION}"
echo "=================================================="

# Add to user json
#	"mcp": {
#		"servers": {
#			"hashing": {
#				"command": "/Users/Data/repos/dump/MCP-Server-for-Hashing/.venv/bin/hashing-mcp-server"
#			},
#			"hashing-docker": {
#				"command": "docker",
#				"args": ["run", "-i", "--rm", "kunalpathak13/hashing-mcp-server:latest"]
#			}
#		}
#	}

# add to /Users/kanad/Library/Application Support/Claude/claude_desktop_config.json

#{
#	"mcpServers": {
#		"hashing": {
#			"command": "/Users/Data/repos/dump/MCP-Server-for-Hashing/.venv/bin/hashing-mcp-server"
#		}
#	}
#}
