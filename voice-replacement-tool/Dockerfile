# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads outputs temp

# Expose port
EXPOSE 5002

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5002

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--timeout", "600", "--workers", "2", "app:app"]
