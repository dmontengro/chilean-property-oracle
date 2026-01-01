FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -e .

COPY src/ src/
COPY data/ data/
COPY models/ models/

EXPOSE 8000

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "property_oracle.api:app", "--host", "0.0.0.0", "--port", "8000"]