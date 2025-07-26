#!/usr/bin/env python3

import asyncio
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)
from pydantic import BaseModel


class AbuseIPDBServer:
    def __init__(self):
        self.server = Server("abuseipdb-mcp-server")
        self.api_key = os.getenv("ABUSEIPDB_API_KEY")
        self.base_url = "https://api.abuseipdb.com/api/v2"
        
        # AbuseIPDB categories mapping
        self.categories = {
            3: "Fraud Orders",
            4: "DDoS Attack",
            5: "FTP Brute-Force",
            6: "Ping of Death",
            7: "Phishing",
            8: "Fraud VoIP",
            9: "Open Proxy",
            10: "Web Spam",
            11: "Email Spam",
            12: "Blog Spam",
            13: "VPN IP",
            14: "Port Scan",
            15: "Hacking",
            16: "SQL Injection",
            17: "Spoofing",
            18: "Brute-Force",
            19: "Bad Web Bot",
            20: "Exploited Host",
            21: "Web App Attack",
            22: "SSH",
            23: "IoT Targeted"
        }
        
        self.setup_handlers()

    def setup_handlers(self):
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            return ListToolsResult(
                tools=[
                    Tool(
                        name="check_ip",
                        description="Check an IP address for abuse reports using AbuseIPDB",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "ipAddress": {
                                    "type": "string",
                                    "description": "A valid IPv4 or IPv6 address to check",
                                },
                                "maxAgeInDays": {
                                    "type": "integer",
                                    "description": "Only return reports within the last x days (1-365)",
                                    "minimum": 1,
                                    "maximum": 365,
                                    "default": 30,
                                },
                                "verbose": {
                                    "type": "boolean",
                                    "description": "Include detailed reports in the response",
                                    "default": False,
                                },
                            },
                            "required": ["ipAddress"],
                        },
                    ),
                    Tool(
                        name="report_ip",
                        description="Report an abusive IP address to AbuseIPDB",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "ip": {
                                    "type": "string",
                                    "description": "A valid IPv4 or IPv6 address to report",
                                },
                                "categories": {
                                    "type": "string",
                                    "description": "Comma separated category IDs (e.g., '18,22')",
                                },
                                "comment": {
                                    "type": "string",
                                    "description": "Descriptive text of the attack (no PII)",
                                },
                                "timestamp": {
                                    "type": "string",
                                    "description": "ISO 8601 datetime of the attack (optional)",
                                },
                            },
                            "required": ["ip", "categories"],
                        },
                    ),
                ]
            )

        @self.server.call_tool()
        async def call_tool(request: CallToolRequest) -> CallToolResult:
            try:
                if request.params.name == "check_ip":
                    return await self.check_ip(request.params.arguments)
                elif request.params.name == "report_ip":
                    return await self.report_ip(request.params.arguments)
                else:
                    raise ValueError(f"Unknown tool: {request.params.name}")
            except Exception as error:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=f"Tool execution failed: {str(error)}"
                        )
                    ],
                    isError=True,
                )

    async def check_ip(self, args: Dict[str, Any]) -> CallToolResult:
        ip_address = args.get("ipAddress")
        max_age_in_days = args.get("maxAgeInDays", 30)
        verbose = args.get("verbose", False)

        if not self.api_key:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="❌ ABUSEIPDB_API_KEY environment variable is required"
                    )
                ],
                isError=True,
            )

        # Validate IP address format
        if not self.is_valid_ip(ip_address):
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="❌ Invalid IP address format"
                    )
                ],
                isError=True,
            )

        # Build query parameters
        params = {
            "ipAddress": ip_address,
            "maxAgeInDays": str(max_age_in_days),
        }

        if verbose:
            params["verbose"] = ""

        url = f"{self.base_url}/check?{urlencode(params)}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={
                        "Key": self.api_key,
                        "Accept": "application/json",
                    },
                )

                data = response.json()

                if not response.is_success:
                    return self.handle_api_error(response, data)

                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=self.format_check_response(data)
                        )
                    ]
                )

        except Exception as error:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"❌ API request failed: {str(error)}"
                    )
                ],
                isError=True,
            )

    async def report_ip(self, args: Dict[str, Any]) -> CallToolResult:
        ip = args.get("ip")
        categories = args.get("categories")
        comment = args.get("comment", "")
        timestamp = args.get("timestamp")

        if not self.api_key:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="❌ ABUSEIPDB_API_KEY environment variable is required"
                    )
                ],
                isError=True,
            )

        # Validate IP address format
        if not self.is_valid_ip(ip):
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="❌ Invalid IP address format"
                    )
                ],
                isError=True,
            )

        # Validate categories
        if not self.is_valid_categories(categories):
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="❌ Categories must be comma-separated integers"
                    )
                ],
                isError=True,
            )

        # Build form data
        form_data = {
            "ip": ip,
            "categories": categories,
            "comment": comment,
        }

        if timestamp:
            form_data["timestamp"] = timestamp

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/report",
                    headers={
                        "Key": self.api_key,
                        "Accept": "application/json",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    data=form_data,
                )

                data = response.json()

                if not response.is_success:
                    return self.handle_api_error(response, data)

                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=self.format_report_response(data)
                        )
                    ]
                )

        except Exception as error:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"❌ API request failed: {str(error)}"
                    )
                ],
                isError=True,
            )

    def handle_api_error(self, response: httpx.Response, data: Dict[str, Any]) -> CallToolResult:
        status = response.status_code
        
        if status == 429:
            retry_after = response.headers.get("Retry-After")
            remaining = response.headers.get("X-RateLimit-Remaining")
            limit = response.headers.get("X-RateLimit-Limit")
            
            error_message = f"Rate limit exceeded ({status})"
            if retry_after:
                error_message += f". Retry after {retry_after} seconds"
            if limit and remaining is not None:
                error_message += f". {remaining}/{limit} requests remaining"
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"❌ {error_message}\n\nError details: {data}"
                    )
                ],
                isError=True,
            )

        error_detail = "Unknown API error"
        if isinstance(data, dict) and "errors" in data and data["errors"]:
            error_detail = data["errors"][0].get("detail", error_detail)
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"❌ API Error ({status}): {error_detail}\n\nFull response: {data}"
                )
            ],
            isError=True,
        )

    def format_check_response(self, data: Dict[str, Any]) -> str:
        ip_data = data["data"]
        
        result = "🔍 **AbuseIPDB Check Results**\n\n"
        result += f"**IP Address:** {ip_data['ipAddress']}\n"
        result += f"**Abuse Confidence Score:** {ip_data['abuseConfidenceScore']}%\n"
        result += f"**Is Public:** {'Yes' if ip_data['isPublic'] else 'No'}\n"
        result += f"**Is Whitelisted:** {'Yes' if ip_data['isWhitelisted'] else 'No'}\n"
        result += f"**Country:** {ip_data['countryName']} ({ip_data['countryCode']})\n"
        result += f"**ISP:** {ip_data['isp']}\n"
        result += f"**Usage Type:** {ip_data['usageType']}\n"
        result += f"**Domain:** {ip_data.get('domain', 'N/A')}\n"
        result += f"**Total Reports:** {ip_data['totalReports']}\n"
        result += f"**Distinct Users:** {ip_data['numDistinctUsers']}\n"
        
        if ip_data.get('lastReportedAt'):
            result += f"**Last Reported:** {ip_data['lastReportedAt']}\n"
        
        if 'isTor' in ip_data:
            result += f"**Is Tor:** {'Yes' if ip_data['isTor'] else 'No'}\n"

        if ip_data.get('reports') and len(ip_data['reports']) > 0:
            result += "\n**Recent Reports:**\n"
            for index, report in enumerate(ip_data['reports'][:5]):
                result += f"\n{index + 1}. **Reported:** {report['reportedAt']}\n"
                
                # Map category numbers to human-readable names
                category_names = []
                for category_id in report['categories']:
                    category_name = self.categories.get(category_id)
                    if category_name:
                        category_names.append(f"{category_id} ({category_name})")
                    else:
                        category_names.append(str(category_id))
                
                result += f"   **Categories:** {', '.join(category_names)}\n"
                result += f"   **Comment:** {report['comment']}\n"
                result += f"   **Reporter Country:** {report['reporterCountryName']}\n"
            
            if len(ip_data['reports']) > 5:
                result += f"\n... and {len(ip_data['reports']) - 5} more reports\n"

        return result

    def format_report_response(self, data: Dict[str, Any]) -> str:
        report_data = data["data"]
        
        result = "✅ **IP Address Reported Successfully**\n\n"
        result += f"**IP Address:** {report_data['ipAddress']}\n"
        result += f"**Updated Abuse Confidence Score:** {report_data['abuseConfidenceScore']}%\n"
        
        return result

    def is_valid_ip(self, ip: str) -> bool:
        """Basic IP validation (IPv4 and IPv6)"""
        ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        ipv6_pattern = r"^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$"
        
        return bool(re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip))

    def is_valid_categories(self, categories: str) -> bool:
        """Check if categories is a comma-separated list of integers"""
        category_pattern = r"^\d+(,\d+)*$"
        return bool(re.match(category_pattern, categories))

    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    server = AbuseIPDBServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main()) 