# Use Python 3.11 alpine image for smaller size
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV MCP_TRANSPORT=stdio

# Copy project files for pip install
COPY pyproject.toml .
COPY requirements.txt .
COPY README.md .
COPY src/ ./src/

# Install the package (creates mcp-abuseipdb entry point)
RUN pip install --no-cache-dir .

# Create non-root user for security (Alpine/BusyBox syntax)
RUN addgroup -g 1001 -S python && \
    adduser -u 1001 -S -G python -h /app -s /bin/sh mcp

# Change ownership of the app directory
RUN chown -R mcp:python /app

# Switch to non-root user
USER mcp

# Expose port for HTTP transport
EXPOSE 8000

# Start via the installed entry point
CMD ["mcp-abuseipdb"]