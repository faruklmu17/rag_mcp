#!/usr/bin/env python3
"""
LLM Client with Dual MCP Integration
Connects Groq LLM to:
1. Custom MCP server (database access)
2. Playwright MCP server (browser automation for any URL)
"""

import asyncio
import json
import os
import sys
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import httpx

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables
load_dotenv()

class DualMCPClient:
    def __init__(self, groq_api_key: str, db_session: ClientSession, pw_session: ClientSession,
                 agile_board_data: list, available_tools: list, model: str = "llama-3.3-70b-versatile"):
        self.groq_api_key = groq_api_key
        self.model = model
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"

        # Store sessions (passed from main)
        self.db_session = db_session
        self.agile_board_data = agile_board_data

        self.pw_session = pw_session
        self.available_tools = available_tools

        # Conversation memory
        self.conversation_history = []
        self.last_page_snapshot = None
        self.last_url = None

    async def call_playwright_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a Playwright MCP tool"""
        if not self.pw_session:
            return {"error": "Playwright MCP not connected"}

        result = await self.pw_session.call_tool(tool_name, arguments)
        return result

    def get_playwright_tools_for_llm(self) -> list:
        """Get Playwright tools in Groq function calling format"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "browser_navigate",
                    "description": "Navigate to a URL in the browser",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to navigate to (e.g., https://google.com)"
                            }
                        },
                        "required": ["url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_snapshot",
                    "description": "Get the accessibility tree snapshot of the current page, showing all interactive elements with their ref identifiers",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_click",
                    "description": "Click an element on the page using its ref identifier from the snapshot",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ref": {
                                "type": "string",
                                "description": "The ref identifier of the element to click (e.g., 'e46')"
                            },
                            "element": {
                                "type": "string",
                                "description": "Human-readable description of the element"
                            }
                        },
                        "required": ["ref", "element"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_type",
                    "description": "Type text into an input field using its ref identifier",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ref": {
                                "type": "string",
                                "description": "The ref identifier of the input field"
                            },
                            "text": {
                                "type": "string",
                                "description": "The text to type"
                            },
                            "element": {
                                "type": "string",
                                "description": "Human-readable description of the element"
                            }
                        },
                        "required": ["ref", "text", "element"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_take_screenshot",
                    "description": "Take a screenshot of the current page",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["png", "jpeg"],
                                "description": "Image format for the screenshot"
                            }
                        },
                        "required": ["type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_press_key",
                    "description": "Press a key on the keyboard (e.g., Enter, Escape, ArrowDown)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "key": {
                                "type": "string",
                                "description": "Name of the key to press (e.g., 'Enter', 'Escape', 'ArrowLeft')"
                            }
                        },
                        "required": ["key"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_hover",
                    "description": "Hover over an element on the page",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ref": {"type": "string", "description": "The ref identifier of the element"},
                            "element": {"type": "string", "description": "Human-readable description"}
                        },
                        "required": ["ref", "element"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_select_option",
                    "description": "Select an option in a dropdown",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ref": {"type": "string", "description": "The ref identifier of the dropdown"},
                            "values": {"type": "array", "items": {"type": "string"}, "description": "Values to select"},
                            "element": {"type": "string", "description": "Human-readable description"}
                        },
                        "required": ["ref", "values", "element"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_wait_for",
                    "description": "Wait for text to appear or disappear, or wait for a specified time",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "Text to wait for"},
                            "textGone": {"type": "string", "description": "Text to wait to disappear"},
                            "time": {"type": "number", "description": "Time to wait in seconds"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "browser_evaluate",
                    "description": "Evaluate JavaScript expression on page",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "function": {"type": "string", "description": "JavaScript function to execute"}
                        },
                        "required": ["function"]
                    }
                }
            }
        ]
    
    async def query_groq_with_tools(self, user_question: str, page_snapshot: str = None, use_tools: bool = True) -> str:
        """Send question to Groq and handle tool calls if needed"""

        # Update last page snapshot if provided
        if page_snapshot:
            self.last_page_snapshot = page_snapshot

        # Build context
        context_parts = [
            "You are an AI assistant with access to:",
            "1. An agile board database (already loaded)",
            "2. Browser automation tools via Playwright MCP",
            "",
            "You can use browser tools to:",
            "- Navigate to URLs",
            "- Get page snapshots (accessibility trees)",
            "- Click elements, type text, press keys",
            "- Take screenshots",
            "- And more!",
            "",
            "When you need to access a webpage, use browser_navigate first, then browser_snapshot to see the page.",
            "Elements in snapshots have 'ref' identifiers (e.g., [ref=e46]) that you use for interactions.",
            "",
            "=== DATABASE DATA ===",
        ]

        if self.agile_board_data:
            context_parts.extend([
                "Agile board assignments:",
                json.dumps(self.agile_board_data, indent=2),
                ""
            ])

        # Add last page snapshot if available
        if self.last_page_snapshot:
            context_parts.extend([
                "",
                "=== CURRENT PAGE SNAPSHOT ===",
                f"URL: {self.last_url}",
                "",
                self.last_page_snapshot[:5000],
                ""
            ])

        context_parts.extend([
            "=== WEB PAGE ANALYSIS ===",
            "You ARE using the official Playwright MCP (Model Context Protocol) server to access web pages!",
            "",
            "How it works:",
            "1. When the user provides a URL, the system uses Playwright MCP's browser_navigate tool",
            "2. Then it calls browser_snapshot to get the accessibility tree of the page",
            "3. The snapshot is sent to you for analysis",
            "",
            "The 'Page snapshot:' you receive contains the REAL DOM from the live webpage,",
            "captured using Microsoft's official @playwright/mcp server.",
            "",
            "You can:",
            "- Identify search boxes, buttons, links, and form fields",
            "- See the text content and structure of the page",
            "- Provide the 'ref' value for elements the user wants to interact with",
            "- Write Playwright test code using the ref values",
            "",
            "Example:",
            "If you see: textbox 'Search' [ref=e46]",
            "You can tell the user: 'The search box has ref=e46'",
            "",
            "When writing Playwright test code, use PYTHON syntax (not JavaScript):",
            "```python",
            "from playwright.async_api import async_playwright",
            "",
            "async def test_example():",
            "    async with async_playwright() as p:",
            "        browser = await p.chromium.launch()",
            "        page = await browser.new_page()",
            "        await page.goto('https://example.com')",
            "        ",
            "        # Use the ref from the snapshot",
            "        await page.locator('[ref=\"e46\"]').fill('search query')",
            "        await page.locator('[ref=\"e69\"]').click()",
            "        ",
            "        await browser.close()",
            "```",
            "",
            "IMPORTANT: When asked if you're using Playwright MCP, say YES!",
            "The page snapshot you receive is from the official Microsoft Playwright MCP server.",
            "",
            "=== YOUR TASK ===",
            "Analyze the page snapshot (if provided) and help the user understand the page structure,",
            "identify elements, and write Playwright test code in PYTHON."
        ])

        system_prompt = "\n".join(context_parts)

        # Build messages with conversation history
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history (last 10 messages to avoid token limits)
        messages.extend(self.conversation_history[-10:])

        # Add current user question
        messages.append({"role": "user", "content": user_question})

        # Get Playwright tools for LLM
        tools = self.get_playwright_tools_for_llm() if use_tools else None

        # Tool calling loop
        max_iterations = 10  # Prevent infinite loops
        iteration = 0

        async with httpx.AsyncClient(timeout=60.0) as client:
            while iteration < max_iterations:
                iteration += 1

                # Prepare request payload
                request_payload = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2000
                }

                # Add tools if enabled
                if tools:
                    request_payload["tools"] = tools
                    request_payload["tool_choice"] = "auto"

                # Send to Groq
                response = await client.post(
                    self.groq_url,
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=request_payload
                )

                if response.status_code != 200:
                    return f"❌ Error: {response.status_code} - {response.text}"

                result = response.json()
                message = result["choices"][0]["message"]

                # Check if LLM wants to call tools
                tool_calls = message.get("tool_calls")

                if not tool_calls:
                    # No more tool calls - we have the final answer
                    assistant_response = message.get("content", "")

                    # Add to conversation history
                    self.conversation_history.append({"role": "user", "content": user_question})
                    self.conversation_history.append({"role": "assistant", "content": assistant_response})

                    return assistant_response

                # LLM wants to call tools
                print(f"\n🔧 LLM is calling {len(tool_calls)} tool(s)...")

                # Add assistant message with tool calls to history
                messages.append(message)

                # Execute each tool call
                for tool_call in tool_calls:
                    tool_name = tool_call["function"]["name"]
                    tool_args = json.loads(tool_call["function"]["arguments"])
                    tool_call_id = tool_call["id"]

                    print(f"   🛠️  {tool_name}({json.dumps(tool_args, indent=2)})")

                    try:
                        # Execute the tool via Playwright MCP
                        tool_result = await self.call_playwright_tool(tool_name, tool_args)

                        # Extract result content
                        if hasattr(tool_result, 'content') and tool_result.content:
                            result_text = tool_result.content[0].text if tool_result.content else str(tool_result)
                        else:
                            result_text = str(tool_result)

                        # Update last page snapshot if this was browser_snapshot
                        if tool_name == "browser_snapshot":
                            self.last_page_snapshot = result_text

                        # Update last URL if this was browser_navigate
                        if tool_name == "browser_navigate" and "url" in tool_args:
                            self.last_url = tool_args["url"]

                        print(f"   ✅ Result: {result_text[:100]}...")

                        # Add tool result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": result_text[:5000]  # Limit size
                        })

                    except Exception as e:
                        error_msg = f"Error executing {tool_name}: {str(e)}"
                        print(f"   ❌ {error_msg}")
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": error_msg
                        })

                # Continue loop to send tool results back to LLM

            # Max iterations reached
            return "⚠️ Maximum tool calling iterations reached. The task may be too complex."

async def main():
    # Get API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ Error: GROQ_API_KEY not found in .env file")
        sys.exit(1)

    print("\n🚀 Starting MCP servers...\n")

    # Start Database MCP
    print("🔌 Starting Database MCP server...")
    db_params = StdioServerParameters(
        command="python3",
        args=["mcp_server.py"],
        env=None
    )

    # Start Playwright MCP
    print("🎭 Starting Playwright MCP server...")
    pw_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp@latest"],
        env=None
    )

    # Use nested async context managers to keep both servers alive
    async with stdio_client(db_params) as (db_read, db_write):
        async with ClientSession(db_read, db_write) as db_session:
            await db_session.initialize()

            # Fetch database data
            result = await db_session.read_resource("assignments://all")
            agile_board_data = json.loads(result.contents[0].text)
            print(f"✅ Database MCP ready! Loaded {len(agile_board_data)} assignments\n")

            async with stdio_client(pw_params) as (pw_read, pw_write):
                async with ClientSession(pw_read, pw_write) as pw_session:
                    await pw_session.initialize()

                    # List available tools
                    tools = await pw_session.list_tools()
                    available_tools = [tool.name for tool in tools.tools]
                    print(f"✅ Playwright MCP ready! {len(available_tools)} tools available")
                    print(f"   Key tools: browser_navigate, browser_snapshot, browser_click, browser_type\n")

                    # Create client with initialized sessions
                    client = DualMCPClient(groq_api_key, db_session, pw_session, agile_board_data, available_tools)

                    print("="*70)
                    print("✅ READY! You can now ask questions about:")
                    print("   📊 Your agile board database")
                    print("   🌐 ANY webpage on the internet")
                    print("="*70)
                    print("\nExamples:")
                    print("  - What assignments does Alice have?")
                    print("  - Go to https://example.com and tell me what's on the page")
                    print("  - Navigate to http://localhost:5500 and compare with database")
                    print("="*70 + "\n")

                    # Interactive loop
                    while True:
                        try:
                            user_input = input("💬 You: ").strip()

                            if not user_input:
                                continue

                            if user_input.lower() in ['quit', 'exit', 'q']:
                                print("\n👋 Goodbye!")
                                break

                            if user_input.lower() in ['clear', 'reset']:
                                client.conversation_history = []
                                client.last_page_snapshot = None
                                client.last_url = None
                                print("\n🧹 Conversation history cleared!\n")
                                continue

                            # LLM-driven tool calling - let the LLM decide what to do
                            print(f"\n🤖 Asking Groq ({client.model}) with tool calling enabled...\n")

                            try:
                                answer = await client.query_groq_with_tools(user_input, use_tools=True)
                                print(f"\n🤖 Assistant:\n{answer}")
                            except Exception as e:
                                print(f"❌ Error: {e}")

                        except KeyboardInterrupt:
                            print("\n\n👋 Goodbye!")
                            break
                        except Exception as e:
                            print(f"\n❌ Error: {e}")
                            import traceback
                            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

