# Quick Start Guide - LLM + MCP Integration

## What You Have Now

Your MCP server can now talk to an LLM (Groq)! Here's how it works:

```
┌─────────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────┐
│   You ask a     │ ───> │ llm_client.py│ ───> │ mcp_server  │ ───> │ SQLite   │
│   question      │      │              │      │             │      │ Database │
└─────────────────┘      └──────────────┘      └─────────────┘      └──────────┘
                                │                                          │
                                │                                          │
                                v                                          │
                         ┌──────────────┐                                  │
                         │  Groq Cloud  │                                  │
                         │  LLM API     │ <────────────────────────────────┘
                         └──────────────┘
                                │
                                v
                         ┌──────────────┐
                         │  Intelligent │
                         │  Answer      │
                         └──────────────┘
```

## Setup (One Time)

### Option 1: Automated Setup (Recommended)

```bash
./setup_llm.sh
```

Then edit `.env` and add your Groq API key.

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install httpx mcp aiosqlite fastmcp python-dotenv
   ```

2. **Initialize the database:**
   ```bash
   python3 init_db.py
   ```

3. **Setup your API key:**
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and replace `your-api-key-here` with your actual key.

   Get your Groq API key from: https://console.groq.com/keys

## Running the LLM Client

Make sure your `.env` file has your API key, then:

```bash
python3 llm_client.py
```

The client will automatically load your API key from the `.env` file.

## Example Session

```
🔌 Connecting to MCP server...
✅ Connected! Available resources: ['assignments://all']
📊 Loaded 9 assignments from database

============================================================
🎯 Agile Board QA Assistant (powered by Groq + MCP)
============================================================

Type your questions about the agile board.
Type 'quit' or 'exit' to end the session.

💬 You: What assignments does Alice Smith have?

🤖 Asking Groq (llama-3.3-70b-versatile)...

🤖 Assistant:
Alice Smith has the following assignments:

1. Implement login form - Status: Developing
2. Add forgot password flow - Status: Under Review
3. Incorrect error message on reset - Status: Ready for QA

She's currently working on 3 different work items across various stages.

💬 You: Are there any items in "Ready for QA" status?

🤖 Assistant:
Yes! There is 1 item in "Ready for QA" status:
- "Incorrect error message on reset" assigned to Alice Smith

This is interesting because "Ready for QA" is not one of the standard 
statuses (Developing, Under Review, Testing, Done) that the tests expect. 
This could indicate a data inconsistency issue.

💬 You: quit

👋 Goodbye!
```

## What Questions Can You Ask?

See `EXAMPLE_QUERIES.md` for a full list of example questions.

Some quick ones:
- "Summarize the agile board"
- "Which engineers are working on defects?"
- "What's in Testing status?"
- "Are there any unusual status values?"
- "What's Alice Smith working on?"

## How MCP Works Here

1. **MCP Server** (`mcp_server.py`):
   - Exposes a resource: `assignments://all`
   - Connects to SQLite database
   - Returns assignment data as JSON

2. **LLM Client** (`llm_client.py`):
   - Connects to MCP server
   - Fetches data from `assignments://all`
   - Sends data + your question to Groq
   - Returns intelligent answer

3. **The Magic**:
   - The LLM has **real-time access** to your database
   - No hardcoded data - always current
   - Can analyze, summarize, and find patterns
   - Understands context and relationships

## Troubleshooting

**"ModuleNotFoundError: No module named 'mcp'"**
```bash
pip install mcp httpx
```

**"Connection refused" or MCP errors**
- Make sure `mcp_server.py` is in the same directory
- Check that the database exists: `ls db/agile_board.db`

**"Invalid API key"**
- Double-check your Groq API key
- Make sure there are no extra spaces

## Next Steps

- Try the example queries in `EXAMPLE_QUERIES.md`
- Modify `mcp_server.py` to expose more resources
- Add more data to the database
- Build a web UI for the chat interface
- Integrate with your CI/CD for automated QA reports

Enjoy! 🚀

