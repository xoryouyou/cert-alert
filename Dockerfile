FROM ghcr.io/astral-sh/uv:alpine

# install cffi for pythons cryptography module
RUN apk update && apk add py3-cffi

# do all the work in /app
ADD . /app
WORKDIR /app
# add folder for reports to be generated to
RUN mkdir reports/
# Install cert-alert and its dependencies using uv
RUN uv sync --locked
RUN uv pip install .

# Default command: run cert-alert with config file
ENTRYPOINT ["uv", "run", "cert-alert"]