FROM python:3.11-slim

# Устанавливаем curl и чистим кэш
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /app/logs

EXPOSE 5000

CMD ["python", "app.py"]