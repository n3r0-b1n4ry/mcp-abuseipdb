# AbuseIPDB MCP Server (Python)

A Model Context Protocol (MCP) server for integrating with the AbuseIPDB API. This server provides two main functions: checking IP addresses for abuse reports and reporting abusive IP addresses.

## Features

- **Check IP**: Query AbuseIPDB for abuse reports on a specific IP address
- **Report IP**: Submit abuse reports for malicious IP addresses  
- **Categories Mapping**: Human-readable category names for abuse reports
- Rate limit handling with detailed error messages
- Comprehensive response formatting
- Input validation for IP addresses and parameters
- **Docker support** for easy deployment and containerization
- **MCP configuration** for seamless integration with MCP clients
- **Async/await support** for better performance
- **Type hints** for better code quality

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
   docker build -t abuseipdb-mcp-server .
   ```

2. **Run the container:**
   ```bash
   docker run -it --rm \
     --name abuseipdb-mcp-server \
     -e ABUSEIPDB_API_KEY="your_api_key_here" \
     abuseipdb-mcp-server
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

- **Lightweight**: Uses Python 3.11 slim base image
- **Secure**: Runs as non-root user
- **Health checks**: Built-in container health monitoring
- **Environment validation**: Validates API key on startup
- **Cross-platform**: Works on Linux, macOS, and Windows

### Claude Desktop Integration

For Claude Desktop, add this to your configuration file:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

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

Or using Docker:
```json
{
  "mcpServers": {
    "abuseipdb": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "--name", "abuseipdb-claude",
        "-e", "ABUSEIPDB_API_KEY",
        "abuseipdb-mcp-server:latest"
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
- `docker build -t abuseipdb-mcp-server .` - Build Docker image
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
├── mcp.json                      # MCP server configuration
├── mcp-docker.json               # Docker-specific MCP configuration
├── mcp-schema.json               # JSON schema for MCP config
├── Dockerfile                    # Docker container definition
├── docker-compose.yml            # Docker Compose configuration
├── docker-run.sh                 # Helper script (Linux/macOS)
├── docker-run.bat                # Helper script (Windows)
├── env.example                   # Environment variables example
└── README.md                     # This file
```

## Production Deployment

### Docker Registry

1. **Tag and push to registry:**
   ```bash
   docker tag abuseipdb-mcp-server your-registry/abuseipdb-mcp-server:latest
   docker push your-registry/abuseipdb-mcp-server:latest
   ```

2. **Deploy on production:**
   ```bash
   docker run -d \
     --name abuseipdb-mcp-prod \
     --restart unless-stopped \
     -e ABUSEIPDB_API_KEY="your_api_key_here" \
     your-registry/abuseipdb-mcp-server:latest
   ```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: abuseipdb-mcp-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: abuseipdb-mcp-server
  template:
    metadata:
      labels:
        app: abuseipdb-mcp-server
    spec:
      containers:
      - name: abuseipdb-mcp-server
        image: abuseipdb-mcp-server:latest
        command: ["python", "src/server.py"]
        env:
        - name: ABUSEIPDB_API_KEY
          valueFrom:
            secretKeyRef:
              name: abuseipdb-secret
              key: api-key
```

## License

MIT 