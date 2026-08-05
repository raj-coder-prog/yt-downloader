# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies including Node.js directly from Debian repositories
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade yt-dlp

# Copy the rest of the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Start the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
