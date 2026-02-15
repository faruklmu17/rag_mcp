# 🤖 Dual MCP + LLM-Driven Browser Automation

An AI-powered system that combines **database access** and **browser automation** using **LLM-driven tool calling** with the **Model Context Protocol (MCP)**.

## 🎯 What This Does

This project demonstrates:
- **LLM-driven browser automation** - The LLM (Groq) decides which Playwright tools to use
- **Dual MCP architecture** - Custom database MCP + Official Playwright MCP running simultaneously
- **Natural language web interaction** - Ask the AI to navigate, analyze, and interact with any website
- **Database + UI comparison** - Compare database state with live web pages
- **Conversation memory** - Multi-turn conversations with context retention

## ✨ Key Features

### 🧠 **LLM-Driven Tool Calling**
The LLM autonomously decides which browser automation tools to use:
- Navigate to any URL
- Analyze page structure (accessibility tree)
- Click elements, type text, press keys
- Take screenshots
- Compare database with UI

### 🔧 **Dual MCP Architecture**
Two MCP servers running simultaneously:
1. **Custom Database MCP** (`mcp_server.py`) - Provides agile board data
2. **Official Playwright MCP** (`@playwright/mcp`) - Provides 10 browser automation tools

### 💬 **Natural Language Interface**
Ask questions in plain English:
```
"Go to https://google.com and tell me what's on the page"
"Navigate to http://localhost:5500 and compare with the database"
"Visit github.com/microsoft/playwright and describe the repository"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                               │
│         "Go to https://google.com"                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              llm_client_playwright.py                       │
│  • Sends user question + tool definitions to Groq LLM       │
│  • Receives tool calls from LLM                             │
│  • Executes tools via Playwright MCP                        │
│  • Sends results back to LLM                                │
│  • Maintains conversation memory                            │
└──┬──────────────────────────────────┬───────────────────────┘
   │                                  │
   │ JSON-RPC (stdio)                 │ HTTPS API
   │                                  │
   ▼                                  ▼
┌──────────────────┐           ┌─────────────┐
│  Playwright MCP  │           │  Groq API   │
│  (@playwright/   │           │             │
│   mcp@latest)    │           │ llama-3.3-  │
│                  │           │ 70b-        │
│  10 Tools:       │           │ versatile   │
│  • navigate      │           │             │
│  • snapshot      │           │ Decides:    │
│  • click         │           │ • Which     │
│  • type          │           │   tools     │
│  • press_key     │           │ • When to   │
│  • screenshot    │           │   call them │
│  • hover         │           └─────────────┘
│  • select        │
│  • wait_for      │
│  • evaluate      │
└────┬─────────────┘
     │
     ▼
┌──────────────────┐           ┌──────────────────┐
│  Chromium        │           │  Database MCP    │
│  Browser         │           │  (mcp_server.py) │
│                  │           │                  │
│  Any webpage     │           │  SQLite DB       │
│  on internet     │           │  Agile board     │
└──────────────────┘           └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+**
- **Node.js 14+** (for Playwright MCP)
- **Groq API Key** - Get one free at https://console.groq.com/keys

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag_mcp
   ```

2. **Install Python dependencies**
   ```bash
   pip install fastmcp aiosqlite httpx mcp python-dotenv
   ```

3. **Install Playwright MCP**
   ```bash
   npm install @playwright/mcp@latest
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Set up your Groq API key**

   Create a `.env` file manually or use the setup script:
   ```bash
   # Manual
   echo "GROQ_API_KEY=your-actual-api-key-here" > .env
   
   # Or use setup script (automatic)
   chmod +x setup_llm.sh
   ./setup_llm.sh
   ```

### 🛠️ Helper Scripts

The project includes several helper scripts to simplify common tasks:

- **`setup_llm.sh`**: Automates dependency installation, database initialization, and `.env` creation.
- **`generate_snapshots.sh`**: Generates fresh accessibility and DOM snapshots for testing.
- **`init_db.py`**: Resets and initializes the SQLite database with sample agile board data.

### Run the Client

**Step-by-step guide to connect MCP to LLM:**

#### **Step 1: Verify Prerequisites**

Make sure you have everything installed:

```bash
# Check Python version (should be 3.7+)
python3 --version

# Check Node.js version (should be 14+)
node --version

# Verify Playwright MCP is installed
ls node_modules/@playwright/mcp
# Should show the package directory

# Verify Python packages are installed
pip list | grep -E "fastmcp|httpx|mcp|python-dotenv"
# Should show: fastmcp, httpx, mcp, python-dotenv

# Verify database exists
ls db/agile_board.db
# Should show: db/agile_board.db
```

#### **Step 2: Set Up Your Groq API Key**

1. **Get your API key** from https://console.groq.com/keys (free account)

2. **Create the `.env` file:**
   ```bash
   echo "GROQ_API_KEY=your-actual-api-key-here" > .env
   ```

3. **Verify the `.env` file:**
   ```bash
   cat .env
   # Should show: GROQ_API_KEY=gsk_...
   ```

#### **Step 3: Start the Client**

```bash
python3 llm_client_playwright.py
```

**What happens when you run this:**

1. **Database MCP starts** - Loads agile board data from SQLite
   ```
   🚀 Starting MCP servers...
   🔌 Starting Database MCP server...
   ✅ Database MCP ready! Loaded 9 assignments
   ```

2. **Playwright MCP starts** - Initializes browser automation tools
   ```
   🎭 Starting Playwright MCP server...
   ✅ Playwright MCP ready! 10 tools available
      Key tools: browser_navigate, browser_snapshot, browser_click, browser_type
   ```

3. **Client is ready** - You can now ask questions!
   ```
   ======================================================================
   ✅ READY! You can now ask questions about:
      📊 Your agile board database
      🌐 ANY webpage on the internet
   ======================================================================

   Examples:
     - What assignments does Alice have?
     - Go to https://example.com and tell me what's on the page
     - Navigate to http://localhost:5500 and compare with database
   ======================================================================

   💬 You: _
   ```

#### **Step 4: Try Your First Query**

**Example 1: Database Query**
```
💬 You: What assignments does Alice have?

🤖 Asking Groq (llama-3.3-70b-versatile) with tool calling enabled...

🤖 Assistant:
Alice Smith has the following assignments:
1. "Implement login form" - Status: Developing
2. "Add forgot password flow" - Status: Under Review
3. "Fix logout bug" - Status: Ready for QA
```

**Example 2: Navigate to a Website**
```
💬 You: Go to https://google.com

🤖 Asking Groq (llama-3.3-70b-versatile) with tool calling enabled...

🔧 LLM is calling 2 tool(s)...
   🛠️  browser_navigate({"url": "https://google.com"})
   ✅ Result: Navigated to https://google.com
   🛠️  browser_snapshot({})
   ✅ Result: navigation "Navigation"...

🤖 Assistant:
I've navigated to Google's homepage. The page has:
- A search box (ref=e46) where you can enter search queries
- A 'Google Search' button (ref=e69)
- An 'I'm Feeling Lucky' button (ref=e70)
- Navigation links for About, Store, Gmail, and Images
```

**Example 3: Multi-Step Automation**
```
💬 You: Go to google.com and search for "weather"

🤖 Asking Groq (llama-3.3-70b-versatile) with tool calling enabled...

🔧 LLM is calling 2 tool(s)...
   🛠️  browser_navigate({"url": "https://google.com"})
   ✅ Result: Navigated successfully
   🛠️  browser_snapshot({})
   ✅ Result: [accessibility tree]

🔧 LLM is calling 2 tool(s)...
   🛠️  browser_type({"ref": "e46", "text": "weather", "element": "Search box"})
   ✅ Result: Typed "weather"
   🛠️  browser_press_key({"key": "Enter"})
   ✅ Result: Pressed Enter

🔧 LLM is calling 1 tool(s)...
   🛠️  browser_snapshot({})
   ✅ Result: [search results]

🤖 Assistant:
I've searched for "weather" on Google. The results show current weather conditions...
```

#### **Step 5: Understanding the Flow**

**What's happening behind the scenes:**

1. **You type a question** → Client receives your input

2. **Client sends to Groq LLM** → Includes:
   - Your question
   - Database data (agile board)
   - Available tools (10 Playwright tools)
   - Conversation history

3. **LLM decides which tools to call** → Example:
   - "Go to google.com" → LLM calls `browser_navigate` + `browser_snapshot`
   - "What assignments does Alice have?" → LLM just analyzes database (no tools)

4. **Client executes tools via MCP** →
   - Sends JSON-RPC request to Playwright MCP
   - Playwright MCP uses real Chromium browser
   - Returns results (page snapshot, navigation status, etc.)

5. **Results sent back to LLM** →
   - LLM analyzes tool results
   - Decides if more tools are needed
   - Returns final answer to you

6. **You see the response** → Natural language answer with context

#### **Step 6: Advanced Usage**

**Clear conversation history:**
```
💬 You: clear
🧹 Conversation history cleared!
```

**Exit the client:**
```
💬 You: quit
👋 Goodbye!
```

**Compare database with UI:**
```
💬 You: Go to http://127.0.0.1:5500/index.html and compare with database

🤖 Assistant:
Comparing database with UI:

✅ MATCHES:
- Alice Smith: "Implement login form" - Developing
- Bob Johnson: "Implement login form" - Testing

❌ DISCREPANCIES:
- Database has "Add forgot password flow" but it's NOT shown on the webpage
```

## 💬 Example Conversations

### **Navigate to Any Website**
```
💬 You: Go to https://google.com

🔧 LLM is calling 2 tool(s)...
   🛠️  browser_navigate({"url": "https://google.com"})
   🛠️  browser_snapshot({})

🤖 Assistant:
I've navigated to Google's homepage. The page has:
- A search box (ref=e46) where you can enter search queries
- A 'Google Search' button (ref=e69)
- An 'I'm Feeling Lucky' button (ref=e70)
- Navigation links for About, Store, Gmail, and Images
```

### **Multi-Step Automation**
```
💬 You: Go to google.com and search for "weather"

🔧 LLM is calling 2 tool(s)...
   🛠️  browser_navigate(...)
   🛠️  browser_snapshot(...)

🔧 LLM is calling 2 tool(s)...
   🛠️  browser_type({"ref": "e46", "text": "weather"})
   🛠️  browser_press_key({"key": "Enter"})

🔧 LLM is calling 1 tool(s)...
   🛠️  browser_snapshot({})

🤖 Assistant:
I've searched for "weather" on Google. The results show current weather conditions...
```

### **Database + UI Comparison**
```
💬 You: Go to http://127.0.0.1:5500/index.html and compare with the database

🔧 LLM is calling 2 tool(s)...
   🛠️  browser_navigate(...)
   🛠️  browser_snapshot(...)

🤖 Assistant:
Comparing database with UI:

✅ MATCHES:
- Alice Smith: "Implement login form" - Developing
- Bob Johnson: "Implement login form" - Testing
- Charlie Liu: "Fix logout bug" - Under Review

❌ DISCREPANCIES:
- Database has "Add forgot password flow" but it's NOT shown on the webpage
```

### **Analyze Any Website**
```
💬 You: Navigate to https://github.com/microsoft/playwright and describe the repository

💬 You: Go to https://stackoverflow.com and find the search box

💬 You: Visit https://news.ycombinator.com and list the top stories
```

## 🎯 What You Can Do

### **Ask About Any Website**
- "Go to https://example.com and tell me what's on the page"
- "Navigate to https://site.com and describe the navigation menu"
- "Visit https://app.com and find all the form fields"

### **Perform Actions**
- "Go to google.com and search for 'Python tutorials'"
- "Navigate to https://site.com and click the login button"
- "Visit https://form.com and fill in the name field with 'John Doe'"

### **Compare Database with UI**
- "Go to http://localhost:5500 and compare with the database"
- "Does the webpage match what's in the database?"
- "Are there any discrepancies between DB and UI?"

### **Multi-Turn Conversations**
```
💬 You: Go to https://google.com
💬 You: What's the ref for the search box?
💬 You: Write a Playwright test to search for "weather"
💬 You: Now add a step to click the first result
```

### **Clear Conversation**
```
💬 You: clear
🧹 Conversation history cleared!
```

## 🛠️ Available Tools

The LLM can autonomously use these 10 Playwright tools:

| Tool | Description |
|------|-------------|
| `browser_navigate` | Navigate to any URL |
| `browser_snapshot` | Get accessibility tree of current page |
| `browser_click` | Click an element by ref |
| `browser_type` | Type text into an input field |
| `browser_press_key` | Press keyboard keys (Enter, Escape, etc.) |
| `browser_take_screenshot` | Take a screenshot |
| `browser_hover` | Hover over an element |
| `browser_select_option` | Select option in dropdown |
| `browser_wait_for` | Wait for text or time |
| `browser_evaluate` | Execute JavaScript |

## 🏗️ How It Works

### **1. LLM-Driven Tool Calling**

The LLM (Groq) decides which tools to use based on your question:

```python
# You ask: "Go to google.com"
# LLM decides: "I need browser_navigate and browser_snapshot"
# LLM returns: tool_calls = [
#   {name: "browser_navigate", args: {url: "https://google.com"}},
#   {name: "browser_snapshot", args: {}}
# ]
```

### **2. Client Executes Tools**

The client executes tools via Playwright MCP:

```python
# Client sends JSON-RPC request to Playwright MCP
result = await playwright_mcp.call_tool("browser_navigate", {"url": "..."})
```

### **3. Playwright MCP Performs Automation**

Playwright MCP uses a real Chromium browser:

```javascript
// Playwright MCP internally does:
await page.goto("https://google.com")
const snapshot = await page.accessibility.snapshot()
```

### **4. Results Sent Back to LLM**

The client sends tool results back to the LLM:

```python
# LLM receives: "Navigated to https://google.com"
# LLM receives: "navigation 'Navigation'\n  link 'About' [ref=e4]\n..."
# LLM analyzes and responds to user
```

## 📊 Database Schema

The custom database MCP provides agile board data:

```sql
engineers (id, name, role)
work_items (id, title, type)
assignments (id, engineer_id, work_item_id, status)
```

**Sample Data:**
- 4 engineers (Alice, Bob, Charlie, Diana)
- 4 work items (login form, logout bug, password flow, error message)
- 9 assignments across different statuses

## 🛠️ Technologies

- **Groq API** - LLM provider (llama-3.3-70b-versatile)
- **Playwright MCP** - Official Microsoft browser automation MCP server
- **FastMCP** - Custom MCP server framework
- **MCP SDK** - Model Context Protocol client
- **SQLite** - Database
- **Python** - Client and custom MCP server
- **Node.js** - Playwright MCP runtime

## 📁 Project Structure

```
rag_mcp/
├── llm_client_playwright.py    # Main client with LLM-driven tool calling
├── mcp_server.py                # Custom database MCP server
├── init_db.py                   # Database initialization
├── index.html                   # Agile board UI (for testing)
├── setup_llm.sh                 # Setup helper script
├── generate_snapshots.sh        # Snapshot generation helper script
├── .env                         # Groq API key (create this)
├── db/
│   └── agile_board.db          # SQLite database
├── scripts/                    # Playwright snapshot scripts
├── snapshots/                  # Generated UI snapshots
├── node_modules/
│   └── @playwright/mcp/        # Official Playwright MCP
├── DUAL_MCP_SETUP.md           # Dual MCP setup guide
├── HOW_TO_USE.md               # Usage guide
├── LLM_DRIVEN_TOOL_CALLING.md  # Tool calling documentation
├── IMPLEMENTATION_SUMMARY.md   # Implementation details
├── PLAYWRIGHT_MCP_TOOLS_REFERENCE.md  # Tool reference
└── CLEANUP_SUMMARY.md          # Project cleanup summary
```

## 📚 Documentation

- **[DUAL_MCP_SETUP.md](DUAL_MCP_SETUP.md)** - Complete dual MCP setup guide
- **[HOW_TO_USE.md](HOW_TO_USE.md)** - Detailed usage instructions
- **[LLM_DRIVEN_TOOL_CALLING.md](LLM_DRIVEN_TOOL_CALLING.md)** - How LLM-driven tool calling works
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[PLAYWRIGHT_MCP_TOOLS_REFERENCE.md](PLAYWRIGHT_MCP_TOOLS_REFERENCE.md)** - All 22 Playwright tools
- **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - Project cleanup summary

## 🎓 Key Concepts

### **Model Context Protocol (MCP)**
Standardized protocol for connecting AI assistants to external data sources and tools.

### **LLM-Driven Tool Calling**
The LLM decides which tools to call based on natural language understanding, not hardcoded logic.

### **Dual MCP Architecture**
Running two MCP servers simultaneously - one for database, one for browser automation.

### **Accessibility Tree**
Structured representation of UI components with `ref` identifiers for each interactive element.

### **Conversation Memory**
Maintaining conversation history and page snapshots across multiple user questions.

## 🎯 Use Cases

- **Web scraping with natural language** - "Go to site.com and extract all product prices"
- **Automated testing** - "Navigate to app.com and verify the login flow works"
- **Data validation** - "Compare database with live webpage"
- **UI analysis** - "Describe the navigation structure of website.com"
- **Form automation** - "Fill out the contact form with my details"

## 🐛 Troubleshooting

### **"Playwright MCP not connected"**
Make sure you installed Playwright MCP:
```bash
npm install @playwright/mcp@latest
```

### **"Groq API error"**
Check your `.env` file has the correct API key:
```bash
cat .env
# Should show: GROQ_API_KEY=gsk_...
```

### **"Database not found"**
Initialize the database:
```bash
python init_db.py
```

## 📄 License

ISC

## 👥 Contributing

Contributions welcome! This project demonstrates:
- LLM-driven browser automation
- Dual MCP architecture
- Natural language web interaction
- Database + UI comparison

Feel free to submit issues and pull requests!