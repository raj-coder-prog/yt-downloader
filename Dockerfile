FROM python:3.11-slim

# Install core extraction utilities needed to unpack binaries
RUN apt-get update && apt-get install -y \
    curl \
    xz-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download and extract standalone Node.js directly into our app directory
RUN mkdir -p /app/node_runtime && \
    curl -sL https://nodejs.org | tar -xJ --strip-components=1 -C /app/node_runtime

# Permanently inject this custom local Node folder directly into the container's environment PATH
ENV PATH="/app/node_runtime/bin:${PATH}"

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade yt-dlp

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
