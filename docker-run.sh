#!/bin/bash

# Helper script to run AbuseIPDB MCP Server (Python) in Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐳 AbuseIPDB MCP Server (Python) Docker Runner${NC}"
echo "=================================================="

# Check if API key is provided
if [ -z "$ABUSEIPDB_API_KEY" ]; then
    echo -e "${RED}❌ Error: ABUSEIPDB_API_KEY environment variable is required${NC}"
    echo "Please set your API key:"
    echo "  export ABUSEIPDB_API_KEY=\"your_api_key_here\""
    echo "  ./docker-run.sh"
    exit 1
fi

# Build the Docker image
echo -e "${YELLOW}🔨 Building Python Docker image...${NC}"
docker build -t abuseipdb-mcp .

# Run the container
echo -e "${YELLOW}🚀 Starting Python container...${NC}"
docker run -it --rm \
    --name abuseipdb-mcp \
    -e ABUSEIPDB_API_KEY="$ABUSEIPDB_API_KEY" \
    abuseipdb-mcp

echo -e "${GREEN}✅ Container stopped${NC}" 