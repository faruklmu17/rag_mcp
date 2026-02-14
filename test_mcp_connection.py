#!/usr/bin/env python3
"""
Test script to verify MCP server connection works
This doesn't require a Groq API key - just tests the MCP part
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_connection():
    """Test that we can connect to MCP server and fetch data"""
    
    print("🧪 Testing MCP Server Connection...")
    print("-" * 50)
    
    try:
        # Setup MCP server connection
        server_params = StdioServerParameters(
            command="python3",
            args=["mcp_server.py"],
            env=None
        )
        
        print("1️⃣  Connecting to MCP server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize session
                await session.initialize()
                print("   ✅ Connected!")
                
                # List available resources
                print("\n2️⃣  Listing available resources...")
                resources = await session.list_resources()
                print(f"   ✅ Found {len(resources.resources)} resource(s):")
                for resource in resources.resources:
                    print(f"      - {resource.uri}")
                
                # Fetch assignments data
                print("\n3️⃣  Fetching assignments data...")
                result = await session.read_resource("assignments://all")
                data = json.loads(result.contents[0].text)
                print(f"   ✅ Retrieved {len(data)} assignments")
                
                # Display sample data
                print("\n4️⃣  Sample data:")
                for i, assignment in enumerate(data[:3], 1):
                    print(f"   {i}. {assignment['engineer']} - {assignment['work_item']} ({assignment['status']})")
                
                if len(data) > 3:
                    print(f"   ... and {len(data) - 3} more")
                
                # Summary
                print("\n" + "=" * 50)
                print("✅ MCP Connection Test PASSED!")
                print("=" * 50)
                print("\nYour MCP server is working correctly!")
                print("You can now run: python3 llm_client.py")
                
                return True
                
    except FileNotFoundError:
        print("\n❌ Error: mcp_server.py not found")
        print("   Make sure you're running this from the project directory")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"   Type: {type(e).__name__}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_mcp_connection())
    exit(0 if success else 1)

