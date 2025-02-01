FROM ghcr.io/astral-sh/uv:alpine

RUN apk update && apk add py3-cffi

ADD . /app
WORKDIR /app
# Install cert-alert and its dependencies using uv
RUN uv sync --locked
RUN uv pip install .

# Copy entrypoint script (optional, for convenience)
COPY config.yml.example ./config.yml

# Default command: run cert-alert with config file
ENTRYPOINT ["uv", "run", "cert-alert"]