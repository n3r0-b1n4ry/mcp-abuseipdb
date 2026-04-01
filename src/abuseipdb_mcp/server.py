#!/usr/bin/env python3

import argparse
import asyncio
import logging
import os
import sys

from .modules import AbuseIPDBServer


def main():
    """Main entry point with transport selection"""
    parser = argparse.ArgumentParser(
        description="AbuseIPDB MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Transport modes:
  stdio   Standard I/O (default) - for MCP clients like Claude Desktop
  http    Streamable HTTP - for remote/multi-client access

Examples:
  mcp-abuseipdb                              # stdio (default)
  mcp-abuseipdb --transport http              # HTTP on 0.0.0.0:8000
  mcp-abuseipdb --transport http --port 3000  # HTTP on custom port
  MCP_TRANSPORT=http mcp-abuseipdb            # via env var
        """
    )
    parser.add_argument(
        "--transport", "-t",
        choices=["stdio", "http"],
        default=None,
        help="Transport type (default: stdio). Can also be set via MCP_TRANSPORT env var"
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Host to bind for HTTP transport (default: 0.0.0.0). Can also be set via MCP_HOST env var"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=None,
        help="Port to bind for HTTP transport (default: 8000). Can also be set via MCP_PORT env var"
    )

    args = parser.parse_args()

    # Priority: CLI arg > env var > default
    transport = args.transport or os.getenv("MCP_TRANSPORT", "stdio")
    host = args.host or os.getenv("MCP_HOST", "0.0.0.0")
    port = args.port or int(os.getenv("MCP_PORT", "8000"))

    server = AbuseIPDBServer()

    if transport == "stdio":
        asyncio.run(server.run())
    elif transport == "http":
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        server.run_http(host=host, port=port)
    else:
        print(f"❌ Unknown transport: {transport}", file=sys.stderr)
        print("   Supported: stdio, http", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
