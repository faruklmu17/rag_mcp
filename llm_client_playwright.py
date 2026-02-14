#!/usr/bin/env python3
"""
LLM Client with Playwright MCP Integration
Connects Groq LLM to:
1. Custom MCP server (database access)
2. Playwright MCP server (browser automation for any URL)
"""

import asyncio
import json
import os
import sys
from typing import Optional
from dotenv import load_dotenv
import httpx

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables
load_dotenv()

class GroqPlaywrightClient:
    def __init__(self, groq_api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.groq_api_key = groq_api_key
        self.model = model
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Database MCP session
        self.db_session: Optional[ClientSession] = None
        self.agile_board_data = None
        
        # Playwright MCP session
        self.playwright_session: Optional[ClientSession] = None
        self.available_tools = []
    
    async def connect_to_database_mcp(self):
        """Connect to custom MCP server for database access"""
        print("🔌 Connecting to Database MCP server...")
        
        server_params = StdioServerParameters(
            command="python3",
            args=["mcp_server.py"],
            env=None
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.db_session = session
                
                # Fetch assignments data from database
                result = await session.read_resource("assignments://all")
                self.agile_board_data = json.loads(result.contents[0].text)
                print(f"✅ Loaded {len(self.agile_board_data)} assignments from database")
                
                return self.agile_board_data
    
    async def connect_to_playwright_mcp(self):
        """Connect to Playwright MCP server for browser automation"""
        print("🎭 Connecting to Playwright MCP server...")
        
        server_params = StdioServerParameters(
            command="npx",
            args=["@playwright/mcp@latest"],
            env=None
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.playwright_session = session
                
                # List available tools
                tools = await session.list_tools()
                self.available_tools = [tool.name for tool in tools.tools]
                print(f"✅ Connected to Playwright MCP! Available tools: {len(self.available_tools)}")
                print(f"   Sample tools: {self.available_tools[:5]}...")
                
                return session
    
    async def query_groq(self, user_question: str) -> str:
        """Send question to Groq with context from both MCP servers"""
        
        # Build context
        context_parts = [
            "You are an AI assistant with access to:",
            "1. An agile board database",
            "2. Playwright browser automation (can access ANY webpage)",
            "",
            "=== DATABASE DATA ===",
        ]
        
        if self.agile_board_data:
            context_parts.extend([
                "Agile board assignments:",
                json.dumps(self.agile_board_data, indent=2),
                ""
            ])
        
        context_parts.extend([
            "=== BROWSER AUTOMATION ===",
            "You can access the DOM of any webpage using Playwright MCP tools.",
            f"Available tools: {', '.join(self.available_tools[:10])}...",
            "",
            "To access a webpage:",
            "1. Use browser_navigate to go to a URL",
            "2. Use browser_snapshot to get the accessibility tree",
            "3. Use browser_take_screenshot for visual inspection",
            "",
            "=== YOUR TASK ===",
            "Answer questions about the agile board OR analyze any webpage the user asks about."
        ])
        
        system_prompt = "\n".join(context_parts)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
        
        # Send to Groq
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                self.groq_url,
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            )
            
            if response.status_code != 200:
                return f"❌ Error: {response.status_code} - {response.text}"
            
            result = response.json()
            return result["choices"][0]["message"]["content"]

async def main():
    # Get API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ Error: GROQ_API_KEY not found in .env file")
        sys.exit(1)
    
    client = GroqPlaywrightClient(groq_api_key)
    
    # Connect to both MCP servers
    print("\n🚀 Starting MCP connections...\n")
    await client.connect_to_database_mcp()
    await client.connect_to_playwright_mcp()
    
    print("\n" + "="*60)
    print("✅ READY! You can now ask questions about:")
    print("   - Your agile board database")
    print("   - ANY webpage on the internet")
    print("="*60 + "\n")
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            print(f"\n🤖 Asking Groq ({client.model})...\n")
            answer = await client.query_groq(user_input)
            print(f"🤖 Assistant:\n{answer}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

