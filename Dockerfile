FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml pyproject.toml
RUN pip install -r --no-cache-dir -r pyproject.toml

COPY src .

RUN python train_model.py

EXPOSE 8000

CMD ["uvicorn", "app:app","--host", "0.0.0.0", "--port", "8000"]

