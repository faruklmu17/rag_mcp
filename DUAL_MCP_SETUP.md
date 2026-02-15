# 🎯 Dual MCP Setup - Database + Browser Automation


## ✅ What You Have Now

Your system uses **TWO MCP servers** working together:

### 1. **Custom Database MCP** (`mcp_server.py`)
- ✅ Queries SQLite database
- ✅ Returns agile board assignments
- ✅ Provides UI snapshots (static files)

### 2. **Official Playwright MCP** (`@playwright/mcp`)
**Source:** [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)

- ✅ Navigates to ANY URL
- ✅ Gets DOM/accessibility tree in real-time
- ✅ Takes screenshots
- ✅ Clicks, types, fills forms
- ✅ 22 browser automation tools (official Microsoft implementation)

---

## 🚀 How to Use

### 1. Test Both MCPs Work:
```bash
python3 test_dual_mcp.py
```

Expected output:
```
✅ Database MCP Resources: ['assignments://all', 'ui://snapshot/accessibility', 'ui://snapshot/html']
✅ Loaded 9 assignments from database
✅ Playwright MCP Tools: 22 available
```

### 2. Run the LLM Client:
```bash
python3 llm_client_playwright.py
```

### 3. Ask Questions!

**Database Questions:**
```
💬 You: What assignments does Alice have?
🤖 Assistant: Alice Smith has 1 assignment: "Implement login form" with status "Developing"
```

**Webpage Analysis:**
```
💬 You: Go to https://example.com and tell me what's on the page
🎭 Navigating to https://example.com...
✅ Navigated successfully!
📸 Getting page snapshot...
🤖 Assistant: [Analyzes the page and describes it]
```

**Compare Database vs UI:**
```
💬 You: Go to http://localhost:5500 and compare it with the database
🎭 Navigating to http://localhost:5500...
🤖 Assistant: [Compares database data with what's shown on the page]
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Question                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          llm_client_playwright.py                       │
│                                                         │
│  ┌──────────────────┐      ┌──────────────────┐       │
│  │  Database MCP    │      │  Playwright MCP  │       │
│  │  (mcp_server.py) │      │  (@playwright/   │       │
│  │                  │      │   mcp@latest)    │       │
│  └────────┬─────────┘      └────────┬─────────┘       │
│           │                         │                  │
└───────────┼─────────────────────────┼──────────────────┘
            │                         │
            ▼                         ▼
    ┌───────────────┐         ┌──────────────┐
    │ SQLite DB     │         │  Chromium    │
    │ (agile board) │         │  Browser     │
    └───────────────┘         └──────────────┘
                                      │
                                      ▼
                              ┌──────────────┐
                              │  ANY Webpage │
                              └──────────────┘
```

---

## 📋 What Each Component Does

### `llm_client_playwright.py`
- Starts both MCP servers simultaneously
- Keeps both sessions alive
- Routes questions to appropriate MCP
- Sends combined context to Groq LLM

### Custom Database MCP
**Resources:**
- `assignments://all` - All database assignments
- `ui://snapshot/accessibility` - Static UI snapshot (JSON)
- `ui://snapshot/html` - Static UI snapshot (HTML)

### Playwright MCP
**Key Tools:**
- `browser_navigate(url)` - Go to any URL
- `browser_snapshot()` - Get accessibility tree
- `browser_take_screenshot()` - Take screenshot
- `browser_click(ref)` - Click element
- `browser_type(ref, text)` - Type text
- `browser_fill_form(fields)` - Fill form
- `browser_console_messages()` - Get console logs
- `browser_network_requests()` - Get network activity

---

## 🎯 Use Cases

### 1. Database Analysis
```
What assignments are in "Ready for QA" status?
Which engineers have the most work?
Summarize the agile board
```

### 2. Web Scraping
```
Go to https://news.ycombinator.com and summarize top stories
Navigate to https://github.com/trending and list top repos
```

### 3. UI Testing
```
Go to http://localhost:5500 and verify all status columns are visible
Navigate to the agile board and check if it matches the database
```

### 4. Combined Analysis
```
Compare the database with what's shown at http://localhost:5500
Are there any discrepancies between DB and UI?
```

---

## 🔧 Configuration

### Environment Variables (.env)
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### MCP Servers
Both servers are spawned automatically by `llm_client_playwright.py`:

**Database MCP:**
```python
command="python3"
args=["mcp_server.py"]
```

**Playwright MCP (Official Config):**
```python
command="npx"
args=["@playwright/mcp@latest"]
```

This matches the [official standard config](https://github.com/microsoft/playwright-mcp#getting-started) exactly!

---

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Make sure `.env` file exists
- Check that it contains: `GROQ_API_KEY=gsk_...`

### "Database MCP failed"
- Check that `db/agile_board.db` exists
- Run: `python3 init_db.py` to recreate database

### "Playwright MCP failed"
- Make sure Node.js is installed
- Run: `npx @playwright/mcp@latest --help` to test

### "Can't navigate to URL"
- Check internet connection
- Try a simple URL first: `https://example.com`
- For localhost, make sure server is running

---

## 📊 Comparison: Old vs New

| Feature | Old (llm_client.py) | New (llm_client_playwright.py) |
|---------|---------------------|--------------------------------|
| Database access | ✅ Yes | ✅ Yes |
| Static snapshots | ✅ Yes | ✅ Yes |
| Navigate to ANY URL | ❌ No | ✅ Yes |
| Real-time DOM | ❌ No | ✅ Yes |
| Browser automation | ❌ No | ✅ Yes |
| Screenshots | ❌ No | ✅ Yes |
| Form interaction | ❌ No | ✅ Yes |

---

## ✅ Summary

You now have:
- ✅ Custom MCP for database queries
- ✅ Official Playwright MCP for browser automation
- ✅ Both working together seamlessly
- ✅ LLM can access database AND any webpage
- ✅ Real-time DOM analysis
- ✅ Full browser automation capabilities

**Run it now:**
```bash
python3 llm_client_playwright.py
```

Then try:
```
Go to https://example.com and describe the page
```

🎉 **You have the best of both worlds!**

---

## 📚 Official Documentation

### Playwright MCP
- **GitHub:** https://github.com/microsoft/playwright-mcp
- **NPM:** https://www.npmjs.com/package/@playwright/mcp
- **All 22 Tools:** See official docs for complete tool reference

### Key Official Tools Available:
1. **Core Automation:** `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`
2. **Form Interaction:** `browser_fill_form`, `browser_select_option`, `browser_file_upload`
3. **Inspection:** `browser_console_messages`, `browser_network_requests`, `browser_take_screenshot`
4. **Advanced:** `browser_evaluate`, `browser_run_code`, `browser_tabs`, `browser_drag`


