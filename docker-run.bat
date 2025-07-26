@echo off
REM Helper script to run AbuseIPDB MCP Server (Python) in Docker (Windows)

echo 🐳 AbuseIPDB MCP Server (Python) Docker Runner
echo ==================================================

REM Check if API key is provided
if "%ABUSEIPDB_API_KEY%"=="" (
    echo ❌ Error: ABUSEIPDB_API_KEY environment variable is required
    echo Please set your API key:
    echo   set ABUSEIPDB_API_KEY=your_api_key_here
    echo   docker-run.bat
    exit /b 1
)

REM Build the Docker image
echo 🔨 Building Python Docker image...
docker build -t abuseipdb-mcp-server .

REM Run the container
echo 🚀 Starting Python container...
docker run -it --rm --name abuseipdb-mcp-server -e ABUSEIPDB_API_KEY=%ABUSEIPDB_API_KEY% abuseipdb-mcp-server

echo ✅ Container stopped 