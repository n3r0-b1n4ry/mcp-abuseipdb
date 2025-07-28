# AbuseIPDB MCP Server (Python)

A Model Context Protocol (MCP) server for integrating with the AbuseIPDB API. This server provides two main functions: checking IP addresses for abuse reports and reporting abusive IP addresses.

## Features

- **Check IP**: Query AbuseIPDB for abuse reports on a specific IP address
- **Report IP**: Submit abuse reports for malicious IP addresses  
- **Categories Mapping**: Human-readable category names for abuse reports
- Rate limit handling with detailed error messages
- Comprehensive response formatting
- Input validation for IP addresses and parameters
- **Alpine Docker support** for lightweight deployment and containerization
- **MCP configuration** for seamless integration with MCP clients
- **Async/await support** for better performance
- **Clean architecture** with simplified error handling

## Setup

### Prerequisites

- Python 3.8 or higher
- Docker (for containerized deployment)
- An AbuseIPDB API key (get one at [abuseipdb.com](https://www.abuseipdb.com/api))

### Local Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your AbuseIPDB API key as an environment variable:
   ```bash
   export ABUSEIPDB_API_KEY="your_api_key_here"
   ```

### Running the Server

```bash
python src/server.py
```

## MCP Configuration

This server includes a complete MCP configuration file (`mcp.json`) that defines:

- **Server metadata**: Name, version, description, and author information
- **Tool definitions**: Complete parameter schemas with validation patterns
- **Environment variables**: Required API key configuration
- **Rate limits**: Documentation of AbuseIPDB API limits by subscription tier
- **Usage examples**: Practical examples for each tool
- **Category reference**: Complete list of AbuseIPDB abuse categories

### Using with MCP Clients

1. **Copy the server configuration** to your MCP client's configuration:
   ```json
   {
     "mcpServers": {
       "abuseipdb": {
         "command": "python",
         "args": ["path/to/abuseipdb-mcp-server/src/server.py"],
         "env": {
           "ABUSEIPDB_API_KEY": "your_api_key_here"
         }
       }
     }
   }
   ```

2. **Test the server**:
   ```bash
   python test/test_server.py
   ```

### MCP Tools Available

The server exposes two tools to MCP clients:

#### `check_ip`
- **Purpose**: Check IP reputation and abuse reports
- **Parameters**: `ipAddress` (required), `maxAgeInDays` (optional), `verbose` (optional)
- **Returns**: Formatted abuse report with confidence score, geolocation, and recent reports

#### `report_ip`  
- **Purpose**: Report abusive IP addresses
- **Parameters**: `ip` (required), `categories` (required), `comment` (optional), `timestamp` (optional)  
- **Returns**: Confirmation with updated abuse confidence score

## Docker Deployment

### Quick Start with Docker

1. **Set your API key:**
   ```bash
   # Linux/macOS
   export ABUSEIPDB_API_KEY="your_api_key_here"
   
   # Windows
   set ABUSEIPDB_API_KEY=your_api_key_here
   ```

2. **Run with helper script:**
   ```bash
   # Linux/macOS
   ./docker-run.sh
   
   # Windows
   docker-run.bat
   ```

### Manual Docker Commands

1. **Build the image:**
   ```bash
   docker build -t abuseipdb-mcp .
   ```

2. **Run the container:**
   ```bash
   docker run -it --rm \
     --name abuseipdb-mcp \
     -e ABUSEIPDB_API_KEY="your_api_key_here" \
     abuseipdb-mcp
   ```

### Docker Compose

1. **Create a `.env` file:**
   ```bash
   cp env.example .env
   # Edit .env and set your API key
   ```

2. **Start with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Stop the service:**
   ```bash
   docker-compose down
   ```

### Docker Features

- **Ultra-lightweight**: Uses Python 3.11 Alpine base image for minimal size
- **Secure**: Runs as non-root user with restricted permissions
- **Fast builds**: Alpine's small footprint reduces build and deployment times
- **Environment validation**: Validates API key on startup
- **Cross-platform**: Works on Linux, macOS, and Windows

### Claude Desktop Integration

For Claude Desktop, add this to your configuration file:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "abuseipdb-python": {
      "command": "python",
      "args": ["path/to/abuseipdb-mcp-server/src/server.py"],
      "env": {
        "ABUSEIPDB_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Or using Docker:
```json
{
  "mcpServers": {
    "abuseipdb-docker": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--name", "abuseipdb-mcp-client",
        "-e", "ABUSEIPDB_API_KEY",
        "abuseipdb-mcp"
      ]
    }
  }
}
```

## Available Tools

### 1. check_ip

Check an IP address for abuse reports.

**Parameters:**
- `ipAddress` (required): A valid IPv4 or IPv6 address
- `maxAgeInDays` (optional): Only return reports within the last x days (1-365, default: 30)
- `verbose` (optional): Include detailed reports in response (default: false)

**Example:**
```json
{
  "ipAddress": "118.25.6.39",
  "maxAgeInDays": 90,
  "verbose": true
}
```

### 2. report_ip

Report an abusive IP address to AbuseIPDB.

**Parameters:**
- `ip` (required): A valid IPv4 or IPv6 address to report
- `categories` (required): Comma-separated category IDs (e.g., "18,22")
- `comment` (optional): Descriptive text of the attack (no PII)
- `timestamp` (optional): ISO 8601 datetime of the attack

**Example:**
```json
{
  "ip": "192.168.1.100",
  "categories": "18,22",
  "comment": "SSH brute force attempts detected",
  "timestamp": "2023-10-18T11:25:11-04:00"
}
```

## API Rate Limits

The server handles rate limits automatically and provides detailed error messages when limits are exceeded. Daily rate limits vary by subscription tier:

| Endpoint | Standard | Webmaster | Supporter | Basic | Premium |
|----------|----------|-----------|-----------|-------|---------|
| check    | 1,000    | 3,000     | 5,000     | 10,000| 50,000  |
| report   | 1,000    | 3,000     | 1,000     | 10,000| 50,000  |

## Error Handling

The server provides comprehensive error handling for:
- Invalid API keys
- Rate limit exceeded (429 errors)
- Invalid IP address formats
- Invalid parameters
- Network errors
- API validation errors
- MCP protocol validation issues (handled gracefully)

## Security Notes

⚠️ **Important**: When reporting IP addresses, ensure you strip any personally identifiable information (PII) from comments. AbuseIPDB is not responsible for any PII you reveal.

## Category Reference

Common abuse categories for reporting:
- 18: Brute Force
- 22: SSH
- 21: FTP Brute Force  
- 11: Comment Spam
- 10: Email Spam
- 5: Mail Server
- 6: Hacking
- 15: Port Scan

For a complete list, visit the [AbuseIPDB categories page](https://www.abuseipdb.com/categories).

## Development

### Available Commands

- `python src/server.py` - Start the MCP server
- `python test/test_server.py` - Run comprehensive tests
- `docker build -t abuseipdb-mcp .` - Build Alpine Docker image
- `docker-compose up --build` - Start with Docker Compose

### Project Structure

```
abuseipdb-mcp-server/
├── src/
│   ├── __init__.py               # Python package initialization
│   └── server.py                 # Main Python MCP server implementation
├── test/
│   └── test_server.py            # Python test suite
├── examples/
│   └── mcp-client-configs.json   # Example MCP client configurations
├── abuseipdb_api_docs/           # Original API documentation
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Python project configuration
├── mcp.json                      # MCP server configuration (Python)
├── mcp-docker.json               # Docker-specific MCP configuration
├── Dockerfile                    # Alpine Docker container definition
├── docker-compose.yml            # Docker Compose configuration
├── docker-run.sh                 # Helper script (Linux/macOS)
├── docker-run.bat                # Helper script (Windows)
├── env.example                   # Environment variables example
└── README.md                     # This file
```

## Architecture

### Server Implementation

The MCP server is built with:
- **Simplified Design**: Clean, minimal implementation without complex error suppression
- **Alpine Docker**: Ultra-lightweight container based on Alpine Linux
- **Async Operations**: Full async/await support for better performance
- **Direct Protocol Handling**: Let the MCP SDK handle protocol validation naturally
- **Robust Validation**: Input validation for IP addresses and categories

### Connection Stability

The server is designed for maximum stability:
- **Clean Protocol Implementation**: Follows MCP standards without interference
- **Minimal Dependencies**: Reduces potential points of failure
- **Error Recovery**: Graceful handling of API and network errors
- **Resource Efficiency**: Alpine base keeps memory and CPU usage low

## Production Deployment

### Docker Registry

1. **Tag and push to registry:**
   ```bash
   docker tag abuseipdb-mcp your-registry/abuseipdb-mcp:latest
   docker push your-registry/abuseipdb-mcp:latest
   ```

2. **Deploy on production:**
   ```bash
   docker run -d \
     --name abuseipdb-mcp-prod \
     --restart unless-stopped \
     -e ABUSEIPDB_API_KEY="your_api_key_here" \
     your-registry/abuseipdb-mcp:latest
   ```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: abuseipdb-mcp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: abuseipdb-mcp
  template:
    metadata:
      labels:
        app: abuseipdb-mcp
    spec:
      containers:
      - name: abuseipdb-mcp
        image: abuseipdb-mcp:latest
        command: ["python", "src/server.py"]
        env:
        - name: ABUSEIPDB_API_KEY
          valueFrom:
            secretKeyRef:
              name: abuseipdb-secret
              key: api-key
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
```

## Troubleshooting

### Common Issues

1. **Connection Closed Errors**: 
   - Ensure API key is properly set
   - Check that the server starts without import errors
   - Verify MCP client configuration

2. **Docker Build Issues**:
   - Make sure you're using the Alpine-compatible syntax
   - Check that all required files are present

3. **API Rate Limits**:
   - Monitor your usage at [AbuseIPDB dashboard](https://www.abuseipdb.com/account)
   - Implement appropriate retry logic in your client

### Debug Mode

To run with additional debugging:
```bash
# Set debug environment
export MCP_DEBUG=1
python src/server.py
```

## License

MIT 