FROM python:3.11-slim

# Install system dependencies and create a permanent symlink for 'node'
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    && ln -s /usr/bin/nodejs /usr/bin/node \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade yt-dlp

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
