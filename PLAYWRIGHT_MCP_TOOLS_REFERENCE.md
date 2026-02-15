# 🎭 Playwright MCP Tools - Quick Reference

> **Source:** [Official Playwright MCP Documentation](https://github.com/microsoft/playwright-mcp)

---

## 🚀 Core Automation Tools

### `browser_navigate`
**Navigate to any URL**
```python
await client.call_playwright_tool("browser_navigate", {
    "url": "https://example.com"
})
```

### `browser_snapshot`
**Get accessibility tree (best for LLM analysis)**
```python
result = await client.call_playwright_tool("browser_snapshot", {})
# Returns structured accessibility tree
```

### `browser_click`
**Click an element**
```python
await client.call_playwright_tool("browser_click", {
    "ref": "element_reference_from_snapshot",
    "element": "Submit button"
})
```

### `browser_type`
**Type text into an element**
```python
await client.call_playwright_tool("browser_type", {
    "ref": "input_reference",
    "text": "Hello World",
    "submit": False  # Set to True to press Enter after
})
```

---

## 📝 Form Interaction

### `browser_fill_form`
**Fill multiple form fields at once**
```python
await client.call_playwright_tool("browser_fill_form", {
    "fields": [
        {"name": "username", "type": "textbox", "ref": "ref1", "value": "john"},
        {"name": "password", "type": "textbox", "ref": "ref2", "value": "secret"}
    ]
})
```

### `browser_select_option`
**Select dropdown option**
```python
await client.call_playwright_tool("browser_select_option", {
    "ref": "dropdown_ref",
    "values": ["option1"]
})
```

### `browser_file_upload`
**Upload files**
```python
await client.call_playwright_tool("browser_file_upload", {
    "paths": ["/absolute/path/to/file.pdf"]
})
```

---

## 🔍 Inspection & Debugging

### `browser_console_messages`
**Get console logs**
```python
result = await client.call_playwright_tool("browser_console_messages", {
    "level": "info"  # "error", "warning", "info", "debug"
})
```

### `browser_network_requests`
**Get network activity**
```python
result = await client.call_playwright_tool("browser_network_requests", {
    "includeStatic": False  # Set True to include images, fonts, etc.
})
```

### `browser_take_screenshot`
**Take a screenshot**
```python
result = await client.call_playwright_tool("browser_take_screenshot", {
    "type": "png",
    "fullPage": True  # Capture entire page
})
```

---

## 🎯 Advanced Interactions

### `browser_hover`
**Hover over element**
```python
await client.call_playwright_tool("browser_hover", {
    "ref": "element_ref",
    "element": "Menu item"
})
```

### `browser_drag`
**Drag and drop**
```python
await client.call_playwright_tool("browser_drag", {
    "startRef": "source_ref",
    "startElement": "Draggable item",
    "endRef": "target_ref",
    "endElement": "Drop zone"
})
```

### `browser_evaluate`
**Run JavaScript**
```python
result = await client.call_playwright_tool("browser_evaluate", {
    "function": "() => { return document.title; }"
})
```

### `browser_run_code`
**Run Playwright code snippet**
```python
result = await client.call_playwright_tool("browser_run_code", {
    "code": "async (page) => { await page.getByRole('button', { name: 'Submit' }).click(); return await page.title(); }"
})
```

---

## ⏱️ Wait & Timing

### `browser_wait_for`
**Wait for conditions**
```python
# Wait for text to appear
await client.call_playwright_tool("browser_wait_for", {
    "text": "Success!"
})

# Wait for text to disappear
await client.call_playwright_tool("browser_wait_for", {
    "textGone": "Loading..."
})

# Wait for time
await client.call_playwright_tool("browser_wait_for", {
    "time": 2  # seconds
})
```

---

## 🗂️ Tab Management

### `browser_tabs`
**Manage browser tabs**
```python
# List all tabs
result = await client.call_playwright_tool("browser_tabs", {
    "action": "list"
})

# Create new tab
await client.call_playwright_tool("browser_tabs", {
    "action": "new"
})

# Switch to tab
await client.call_playwright_tool("browser_tabs", {
    "action": "select",
    "index": 1
})

# Close tab
await client.call_playwright_tool("browser_tabs", {
    "action": "close",
    "index": 1
})
```

---

## 🎨 All 22 Official Tools

1. `browser_navigate` - Navigate to URL
2. `browser_snapshot` - Get accessibility tree ⭐
3. `browser_click` - Click element
4. `browser_type` - Type text
5. `browser_fill_form` - Fill multiple fields
6. `browser_select_option` - Select dropdown
7. `browser_file_upload` - Upload files
8. `browser_console_messages` - Get console logs
9. `browser_network_requests` - Get network activity
10. `browser_take_screenshot` - Take screenshot
11. `browser_hover` - Hover over element
12. `browser_drag` - Drag and drop
13. `browser_evaluate` - Run JavaScript
14. `browser_run_code` - Run Playwright code
15. `browser_wait_for` - Wait for conditions
16. `browser_tabs` - Manage tabs
17. `browser_press_key` - Press keyboard key
18. `browser_handle_dialog` - Handle alerts/dialogs
19. `browser_navigate_back` - Go back in history
20. `browser_resize` - Resize browser window
21. `browser_close` - Close browser
22. `browser_install` - Install browser

---

## 💡 Best Practices

1. **Use `browser_snapshot` for actions** - More reliable than screenshots
2. **Use exact `ref` from snapshots** - Ensures deterministic behavior
3. **Wait for elements** - Use `browser_wait_for` before interactions
4. **Check console/network** - Debug issues with inspection tools
5. **Handle dialogs** - Use `browser_handle_dialog` for alerts

---

## 📚 Learn More

- **Official Docs:** https://github.com/microsoft/playwright-mcp
- **Playwright Docs:** https://playwright.dev
- **MCP Protocol:** https://modelcontextprotocol.io

