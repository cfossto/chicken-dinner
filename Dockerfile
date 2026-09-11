FROM python:3.10-slim

# Grab the uv/uvx binaries from the official distroless image
COPY --from=ghcr.io/astral-sh/uv:0.8.12 /uv /uvx /bin/

WORKDIR /app

# Install dependencies first so the layer is cached when only source changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Copy the rest of the project (README.md is required as the package readme)
COPY README.md ./README.md
COPY src ./src
COPY results.csv ./results.csv

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "src/chicken_dinner/main.py", "--host", "0.0.0.0", "--port", "8000"]
