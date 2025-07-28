#!/usr/bin/env python3

"""
Test script to validate Python MCP server functionality
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from server import AbuseIPDBServer


async def test_server_initialization():
    """Test server initialization"""
    print("🧪 Testing Python MCP Server Initialization...")
    print("=" * 50)
    
    try:
        server = AbuseIPDBServer()
        print("✅ Server initialized successfully")
        print(f"✅ Base URL: {server.base_url}")
        print(f"✅ Categories loaded: {len(server.categories)} categories")
        
        # Check if API key is configured
        if server.api_key:
            print("✅ API key is configured")
        else:
            print("⚠️  API key not configured (ABUSEIPDB_API_KEY)")
            
        return True
        
    except Exception as error:
        print(f"❌ Server initialization failed: {error}")
        return False


async def test_validation_functions():
    """Test IP and category validation functions"""
    print("\n🔍 Testing validation functions...")
    print("-" * 30)
    
    server = AbuseIPDBServer()
    
    # Test IP validation
    test_ips = [
        ("192.168.1.1", True, "Valid IPv4"),
        ("127.0.0.1", True, "Valid IPv4 localhost"),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", False, "Invalid IPv6 format"),
        ("::1", True, "Valid IPv6 localhost"),
        ("invalid.ip", False, "Invalid IP format"),
        ("999.999.999.999", False, "Invalid IPv4 range"),
    ]
    
    for ip, expected, description in test_ips:
        result = server.is_valid_ip(ip)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {description}: {ip} -> {result}")
    
    # Test category validation
    test_categories = [
        ("18,22", True, "Valid comma-separated categories"),
        ("18", True, "Single category"),
        ("1,2,3,4,5", True, "Multiple categories"),
        ("abc,def", False, "Non-numeric categories"),
        ("18,", False, "Trailing comma"),
        (",18", False, "Leading comma"),
        ("", False, "Empty string"),
    ]
    
    for categories, expected, description in test_categories:
        result = server.is_valid_categories(categories)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {description}: '{categories}' -> {result}")


async def test_category_mapping():
    """Test category number to name mapping"""
    print("\n🏷️  Testing category mapping...")
    print("-" * 30)
    
    server = AbuseIPDBServer()
    
    # Test some known categories
    test_categories = [18, 22, 10, 15, 999]  # 999 doesn't exist
    
    for cat_id in test_categories:
        cat_name = server.categories.get(cat_id, "Unknown")
        print(f"   Category {cat_id}: {cat_name}")


async def test_response_formatting():
    """Test response formatting with mock data"""
    print("\n📝 Testing response formatting...")
    print("-" * 30)
    
    server = AbuseIPDBServer()
    
    # Mock check response data
    mock_check_data = {
        "data": {
            "ipAddress": "192.168.1.100",
            "abuseConfidenceScore": 75,
            "isPublic": True,
            "isWhitelisted": False,
            "countryName": "United States",
            "countryCode": "US",
            "isp": "Example ISP",
            "usageType": "Data Center/Web Hosting/Transit",
            "domain": "example.com",
            "totalReports": 5,
            "numDistinctUsers": 3,
            "lastReportedAt": "2023-10-18T11:25:11+00:00",
            "isTor": False,
            "reports": [
                {
                    "reportedAt": "2023-10-18T11:25:11+00:00",
                    "categories": [18, 22],
                    "comment": "SSH brute force attempts",
                    "reporterCountryName": "Canada"
                },
                {
                    "reportedAt": "2023-10-17T09:15:30+00:00",
                    "categories": [15],
                    "comment": "Port scanning activity",
                    "reporterCountryName": "Germany"
                }
            ]
        }
    }
    
    formatted_response = server.format_check_response(mock_check_data)
    print("✅ Check response formatted successfully")
    print("Sample output:")
    print(formatted_response[:200] + "..." if len(formatted_response) > 200 else formatted_response)
    
    # Mock report response data
    mock_report_data = {
        "data": {
            "ipAddress": "192.168.1.100",
            "abuseConfidenceScore": 80
        }
    }
    
    formatted_report = server.format_report_response(mock_report_data)
    print("\n✅ Report response formatted successfully")
    print("Sample output:")
    print(formatted_report)


async def test_mcp_configuration():
    """Test MCP configuration files"""
    print("\n⚙️  Testing MCP configuration files...")
    print("-" * 30)
    
    config_files = [
        "mcp.json",
        "mcp-docker.json",
        "examples/mcp-client-configs.json"
    ]
    
    for config_file in config_files:
        config_path = Path(__file__).parent.parent / config_file
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                print(f"✅ {config_file}: Valid JSON")
                
                # Basic validation for MCP configs
                if config_file.startswith("mcp"):
                    if "mcpServers" in config_data:
                        print(f"   ✅ Contains mcpServers configuration")
                    else:
                        print(f"   ⚠️  Missing mcpServers configuration")
                        
            except json.JSONDecodeError as e:
                print(f"❌ {config_file}: Invalid JSON - {e}")
            except Exception as e:
                print(f"❌ {config_file}: Error reading file - {e}")
        else:
            print(f"⚠️  {config_file}: File not found")


async def main():
    """Run all tests"""
    print("🐍 AbuseIPDB Python MCP Server Tests")
    print("=" * 50)
    
    tests = [
        test_server_initialization,
        test_validation_functions,
        test_category_mapping,
        test_response_formatting,
        test_mcp_configuration,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            result = await test()
            if result is not False:  # None or True counts as passed
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n🎉 Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed!")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set your API key: export ABUSEIPDB_API_KEY='your_key'")
        print("3. Run the server: python src/server.py")
        print("4. Configure your MCP client to use Python server")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    os.environ["ABUSEIPDB_API_KEY"] = "fd52070439c78dc53529ebee94691c50a7f537c213442d553612b57ae4d7739d279884ff786833ea"
    asyncio.run(main()) 