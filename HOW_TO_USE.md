# 🚀 How to Use the Dual MCP Client

**Your LLM can now access both your database AND any webpage!**

---

## ✅ What Was Fixed

### Problem:
- URLs weren't being detected when you just pasted them
- The LLM was just talking about navigating, not actually doing it

### Solution:
- ✅ **Improved URL detection** - Now detects URLs anywhere in your input
- ✅ **Better prompts** - LLM now understands page snapshots and can analyze them
- ✅ **Automatic navigation** - When you paste a URL, it automatically navigates

---

## 🎯 How to Use It

### 1. Start the Client

```bash
python3 llm_client_playwright.py
```

You'll see:
```
✅ Database MCP ready! Loaded 9 assignments
✅ Playwright MCP ready! 22 tools available
✅ READY! You can now ask questions...
```

---

### 2. Ask Questions

#### **Database Questions** (No URL needed)
```
💬 You: What assignments does Alice have?
💬 You: How many items are in "Ready for QA" status?
💬 You: Summarize the agile board
```

#### **Web Page Analysis** (Just paste the URL!)
```
💬 You: https://www.google.com
```

The client will:
1. 🎭 Navigate to the URL
2. 📸 Get the page snapshot (accessibility tree)
3. 🤖 Send it to the LLM for analysis

#### **Ask Questions About the Page**
```
💬 You: https://www.google.com

🤖 Assistant: [Analyzes the page]

💬 You: What is the ref for the search box?

🤖 Assistant: The search box has ref=5

💬 You: Write a Playwright test to search for "today's weather"

🤖 Assistant: Here's the test code:
```python
await page.locator('[ref="5"]').fill("today's weather")
await page.locator('[ref="5"]').press("Enter")
```
```

---

## 📝 Example Session

```
💬 You: https://www.google.com

🎭 Navigating to https://www.google.com...
✅ Navigated successfully!
📸 Getting page snapshot...

🤖 Analyzing with Groq (llama-3.3-70b-versatile)...

🤖 Assistant:
I can see the Google homepage. The page has:
- A search box (ref=5) labeled "Search"
- A "Google Search" button (ref=8)
- An "I'm Feeling Lucky" button (ref=9)
- Various navigation links

What would you like to do with this page?

💬 You: Write a Playwright test to search for "today's weather"

🤖 Assistant:
Here's a Playwright test to search for "today's weather":

```python
import asyncio
from playwright.async_api import async_playwright

async def test_google_search():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Navigate to Google
        await page.goto("https://www.google.com")
        
        # Fill in the search box
        await page.locator('[ref="5"]').fill("today's weather")
        
        # Press Enter to search
        await page.locator('[ref="5"]').press("Enter")
        
        # Wait for results
        await page.wait_for_load_state("networkidle")
        
        await browser.close()

asyncio.run(test_google_search())
```

This test:
1. Opens Google
2. Finds the search box using ref=5
3. Types "today's weather"
4. Presses Enter to search
```

---

## 🎯 Tips for Best Results

### ✅ DO:
1. **Just paste the URL** - No need to say "go to" or "navigate to"
2. **Ask specific questions** - "What is the ref for the search box?"
3. **Request test code** - "Write a Playwright test to click the login button"
4. **Use follow-up questions** - The page snapshot stays loaded

### ❌ DON'T:
1. **Don't expect the LLM to click** - It analyzes the page, you write the test
2. **Don't paste multiple URLs at once** - One at a time
3. **Don't expect real-time updates** - The snapshot is static

---

## 🔧 Troubleshooting

### "❌ No URL found in your question"
- Make sure the URL starts with `http://` or `https://`
- Example: `https://www.google.com` ✅
- Example: `www.google.com` ❌

### "❌ Error navigating"
- Check your internet connection
- Make sure the URL is valid
- Try a simpler URL first (like `https://example.com`)

### LLM doesn't understand the page
- The snapshot might be too large (truncated to 5000 chars)
- Try asking more specific questions
- Ask for specific element refs

---

## 🎉 What You Can Do Now

1. **Analyze any webpage** - Just paste the URL
2. **Find element refs** - Ask "What is the ref for the X button?"
3. **Write Playwright tests** - Ask "Write a test to click X and type Y"
4. **Compare DB vs UI** - Navigate to `http://localhost:5500` and compare with database
5. **Learn page structure** - Ask "What elements are on this page?"

---

## 🚀 Next Steps

Try these examples:

```bash
# Example 1: Analyze Google
💬 You: https://www.google.com
💬 You: What elements can I interact with?

# Example 2: Write a test
💬 You: https://www.google.com
💬 You: Write a Playwright test to search for "Python tutorials"

# Example 3: Compare DB vs UI
💬 You: http://localhost:5500
💬 You: Compare this page with the database assignments
```

---

**You're all set!** 🎊

Run `python3 llm_client_playwright.py` and start exploring!

