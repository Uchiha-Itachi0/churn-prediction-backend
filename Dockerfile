FROM python:3.8

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install daphne  # Add this line

# Copy project files
COPY . .

# Create media and static directories
RUN mkdir -p media static

EXPOSE 8000

# Command will be overridden by docker-compose
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]