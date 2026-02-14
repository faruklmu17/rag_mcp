#!/usr/bin/env python3
"""
LLM Client that connects MCP Server to Groq Cloud API
Allows the LLM to query the agile board through MCP
"""

import asyncio
import json
import os
import sys
from typing import Optional
import subprocess

# Check for required packages
try:
    import httpx
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from dotenv import load_dotenv
except ImportError:
    print("❌ Missing required packages. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx", "mcp", "python-dotenv"])
    import httpx
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GroqMCPClient:
    def __init__(self, groq_api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.groq_api_key = groq_api_key
        self.model = model
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
        self.mcp_session: Optional[ClientSession] = None
        self.agile_board_data = None
        self.ui_accessibility_snapshot = None
        self.ui_html_snapshot = None
        
    async def connect_to_mcp(self):
        """Connect to the MCP server and fetch agile board data + UI snapshots"""
        print("🔌 Connecting to MCP server...")

        server_params = StdioServerParameters(
            command="python3",
            args=["mcp_server.py"],
            env=None
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                self.mcp_session = session

                # List available resources
                resources = await session.list_resources()
                print(f"✅ Connected! Available resources: {[r.uri for r in resources.resources]}")

                # Fetch assignments data from database
                result = await session.read_resource("assignments://all")
                self.agile_board_data = json.loads(result.contents[0].text)
                print(f"📊 Loaded {len(self.agile_board_data)} assignments from database")

                # Fetch UI accessibility snapshot
                try:
                    result = await session.read_resource("ui://snapshot/accessibility")
                    self.ui_accessibility_snapshot = json.loads(result.contents[0].text)
                    print(f"🎨 Loaded UI accessibility snapshot")
                except Exception as e:
                    print(f"⚠️  UI accessibility snapshot not available: {e}")
                    self.ui_accessibility_snapshot = None

                # Fetch UI HTML snapshot
                try:
                    result = await session.read_resource("ui://snapshot/html")
                    self.ui_html_snapshot = result.contents[0].text
                    print(f"📄 Loaded UI HTML snapshot ({len(self.ui_html_snapshot)} chars)")
                except Exception as e:
                    print(f"⚠️  UI HTML snapshot not available: {e}")
                    self.ui_html_snapshot = None

                return self.agile_board_data
    
    async def query_groq(self, user_question: str) -> str:
        """Send question to Groq with agile board context + UI snapshots"""

        if not self.agile_board_data:
            return "❌ Error: No agile board data loaded. Please connect to MCP first."

        # Build context for the LLM
        context_parts = [
            "You are an AI assistant helping with agile board analysis and QA.",
            "",
            "=== DATABASE DATA ===",
            "You have access to the following agile board data from the database:",
            json.dumps(self.agile_board_data, indent=2),
            "",
            "The database contains assignments with:",
            "- engineer: Name of the engineer",
            "- work_item: Title of the work item (story or defect)",
            "- status: Current status (Developing, Under Review, Testing, Done, Ready for QA)",
        ]

        # Add UI accessibility snapshot if available
        if self.ui_accessibility_snapshot:
            # Extract status columns from accessibility tree
            statuses_in_ui = []
            if "children" in self.ui_accessibility_snapshot:
                for node in self.ui_accessibility_snapshot["children"]:
                    if node.get("role") == "heading" and node.get("level") == 3:
                        statuses_in_ui.append(node.get("name"))

            context_parts.extend([
                "",
                "=== UI SNAPSHOT (What users see) ===",
                f"The UI displays {len(statuses_in_ui)} status columns:",
                json.dumps(statuses_in_ui, indent=2),
                "",
                "Full UI accessibility tree:",
                json.dumps(self.ui_accessibility_snapshot, indent=2)[:2000] + "..."  # Truncate to save tokens
            ])

        # Add note about UI HTML if available
        if self.ui_html_snapshot:
            context_parts.extend([
                "",
                "=== UI HTML DOM ===",
                f"UI HTML snapshot is available ({len(self.ui_html_snapshot)} characters)",
                "The HTML contains the rendered DOM structure of the agile board."
            ])

        context_parts.extend([
            "",
            "=== YOUR TASK ===",
            "Answer questions about the agile board, analyze the data, identify discrepancies between",
            "the database and UI, and provide insights. If you notice differences between what's in the",
            "database vs what's shown in the UI, point them out!"
        ])

        system_prompt = "\n".join(context_parts)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question}
        ]
        
        print(f"\n🤖 Asking Groq ({self.model})...")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
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
                    "max_tokens": 1024
                }
            )
            
            if response.status_code != 200:
                return f"❌ Groq API Error: {response.status_code} - {response.text}"
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def interactive_mode(self):
        """Run interactive Q&A session"""
        print("\n" + "="*60)
        print("🎯 Agile Board QA Assistant (powered by Groq + MCP)")
        print("="*60)
        print("\nType your questions about the agile board.")
        print("Type 'quit' or 'exit' to end the session.\n")
        
        while True:
            try:
                question = input("\n💬 You: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if not question:
                    continue
                
                answer = await self.query_groq(question)
                print(f"\n🤖 Assistant:\n{answer}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


async def main():
    # Get Groq API key from .env file
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        print("\nPlease create a .env file with your API key:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Groq API key to the .env file")
        print("  3. Get your key from: https://console.groq.com/keys")
        print("\nOr enter your API key now:")
        groq_api_key = input("API Key: ").strip()

        if not groq_api_key:
            print("❌ No API key provided. Exiting.")
            return
    else:
        print(f"✅ Loaded API key from .env file")
    
    # Initialize client
    client = GroqMCPClient(groq_api_key)
    
    # Connect to MCP and load data
    await client.connect_to_mcp()
    
    # Start interactive session
    await client.interactive_mode()


if __name__ == "__main__":
    asyncio.run(main())

