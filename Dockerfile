# Use an official Python runtime as a parent image
# Using '-slim' reduces image size compared to the full image
FROM python:3.13-slim AS base

# Set environment variables using the recommended KEY=VALUE format
# Prevents python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# --- Security: Create a non-root user ---
# Running as non-root user is a security best practice
RUN adduser --system --group appuser

# --- Copy Files Needed for Build/Installation ---
# Copy essential project definition and metadata files first
# This leverages Docker cache better if these files don't change often
COPY pyproject.toml README.md LICENSE ./
# Ensure the LICENSE file exists in your project root or remove it from the COPY line if it doesn't

# Copy the source code needed for the installation
COPY ./src /app/src

# --- Install Dependencies ---
# Install the package defined in pyproject.toml from the local files now present in /app
# This command will build the package using hatchling, which now has access to README.md and src/
RUN pip install --no-cache-dir .

# --- Final Configuration ---
# Switch to the non-root user for execution
USER appuser

# --- Define the entrypoint ---
# Specify the command to run when the container starts
# **IMPORTANT:** Ensure this matches the script name defined in pyproject.toml [project.scripts]
# Your pyproject.toml defines "hashing-mcp-server", not "hashing-mcp"
ENTRYPOINT ["hashing-mcp-server"]

# --- Build Command Reminder ---
# Build the file with: docker build -t kunalpathak13/hashing-mcp-server:1.6.0 .
# Push image to Docker Hub with: docker push kunalpathak13/hashing-mcp-server:1.6.0
