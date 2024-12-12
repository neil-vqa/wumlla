FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.8 /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN uv pip install --system -r pyproject.toml

CMD ["python", "serve.py"]