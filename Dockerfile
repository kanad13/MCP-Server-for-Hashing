# Use a Python image matching your .python-version
# Using 3.13 slim variant assuming it's available or adapting as needed
# If a specific uv image for 3.13 isn't available yet, build uv in a stage
FROM python:3.13-slim-bookworm AS base
RUN pip install uv

FROM base AS uv-builder
# Install the project into `/app`
WORKDIR /app

# Copy project definition files
COPY pyproject.toml ./
# If you create a uv.lock file later, copy it too:
# COPY uv.lock ./

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking (good practice in Docker)
ENV UV_LINK_MODE=copy

# Install dependencies using uv sync (will create a venv in ./.venv)
# Mount cache for faster builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv && \
    . .venv/bin/activate && \
    uv pip install --system .[dev] # Install including dev deps needed for tests if run in docker

# Add the rest of the project source code
COPY src ./src
COPY test ./test

# Final stage using a clean Python base
FROM base AS final
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=uv-builder /app/.venv ./.venv
# Copy the application code
COPY --from=uv-builder /app/src ./src
COPY --from=uv-builder /app/pyproject.toml ./

# Set PATH to include the venv bin directory
ENV PATH="/app/.venv/bin:$PATH"

# Set the entrypoint to run the MCP server script
# This uses the script defined in pyproject.toml
ENTRYPOINT ["hashing-mcp-server"]

# Expose default MCP ports if needed, although stdio transport doesn't use them
# EXPOSE 6112

# Optional: Add a non-root user
# RUN useradd --create-home appuser
# USER appuser
