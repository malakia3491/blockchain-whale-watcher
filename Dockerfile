FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN pip install uv
RUN uv pip install --system -r pyproject.toml

COPY . .

CMD ["sh", "-c", "alembic upgrade head && python main.py"]