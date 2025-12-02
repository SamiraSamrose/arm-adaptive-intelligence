FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY config/ ./config/
COPY setup.py .
COPY README.md .

# Install package
RUN pip install -e .

# Expose ports for Python bridge
EXPOSE 5000

# Run example
CMD ["python", "example_usage.py"]
