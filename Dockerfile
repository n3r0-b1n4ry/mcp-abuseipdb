# Use Python 3.11 alpine image for smaller size
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    && apk del .build-deps

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create non-root user for security (Alpine/BusyBox syntax)
RUN addgroup -g 1001 -S python && \
    adduser -u 1001 -S -G python -h /app -s /bin/sh mcp

# Change ownership of the app directory
RUN chown -R mcp:python /app

# Switch to non-root user
USER mcp

# Start the Python MCP server
CMD ["python", "src/server.py"] 