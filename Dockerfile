# Stage 1: Get the official Node image to copy its files
FROM node:20-slim AS node_source

# Stage 2: Build our actual Python application container
FROM python:3.11-slim

# Copy the pre-built, ready-to-use Node.js binaries directly from Stage 1
COPY --from=node_source /usr/local/bin/node /usr/local/bin/node
COPY --from=node_source /usr/local/lib/node_modules /usr/local/lib/node_modules

WORKDIR /app

# Install standard requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade yt-dlp

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
