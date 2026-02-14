# DOM Analysis Guide - LLM Can Now See Both Database AND UI!

## 🎉 What's New

Your LLM client can now access **THREE data sources**:

1. ✅ **Database** - Real assignment data from SQLite
2. ✅ **UI Accessibility Tree** - What the UI displays (structured)
3. ✅ **UI HTML DOM** - The actual HTML rendered in the browser

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Question                             │
│   "Does the UI match the database?"                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  llm_client.py                               │
│  Fetches from MCP Server:                                    │
│  1. Database assignments                                     │
│  2. UI accessibility snapshot                                │
│  3. UI HTML snapshot                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│ mcp_server.py│          │  Groq Cloud  │
│              │          │   LLM API    │
│ 3 Resources: │          │              │
│ - DB data    │          │ Analyzes ALL │
│ - UI a11y    │          │ 3 sources    │
│ - UI HTML    │          │              │
└──────────────┘          └──────┬───────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Intelligent Comparison Answer                   │
│  "The database has 9 assignments with 5 statuses,            │
│   but the UI only shows 5 columns. There's a match!"         │
└─────────────────────────────────────────────────────────────┘
```

## MCP Resources Available

Your MCP server now exposes:

1. **`assignments://all`** - Database assignments
2. **`ui://snapshot/accessibility`** - UI accessibility tree (JSON)
3. **`ui://snapshot/html`** - Full HTML DOM

## Example Questions You Can Now Ask

### Database vs UI Comparison:
- "Does the UI match the database?"
- "Are there any statuses in the database that aren't shown in the UI?"
- "Compare the database assignments with what's displayed in the UI"
- "Are there discrepancies between the DB and UI?"

### UI-Specific Questions:
- "What status columns are shown in the UI?"
- "How many columns does the UI display?"
- "What's the structure of the UI?"

### Database-Specific Questions:
- "What assignments does Alice have in the database?"
- "Which statuses exist in the database?"

### Combined Analysis:
- "Is the 'Ready for QA' status visible in the UI?"
- "Find all data inconsistencies between database and UI"
- "Generate a QA report comparing DB vs UI"

## How to Use

### 1. Make Sure Snapshots Exist

Check if snapshots are available:
```bash
ls -lh snapshots/
```

You should see:
- `ui_snapshot.json` - Accessibility tree
- `ui_snapshot.html` - HTML DOM

### 2. Generate New Snapshots (if needed)

If you update the UI and want fresh snapshots:

```bash
# Start a web server for index.html
python3 -m http.server 5500

# In another terminal, generate snapshots
./generate_snapshots.sh
```

Or manually:
```bash
npx playwright test scripts/snapshot_accessibility.spec.ts
npx playwright test scripts/snapshot_dom.spec.ts
```

### 3. Run the LLM Client

```bash
python3 llm_client.py
```

The client will automatically load:
- ✅ Database data
- ✅ UI accessibility snapshot
- ✅ UI HTML snapshot

### 4. Ask Comparison Questions!

```
💬 You: Does the UI match the database?

🤖 Assistant:
Let me compare the database and UI...

DATABASE: Contains 9 assignments with 5 distinct statuses:
- Developing
- Under Review
- Testing
- Done
- Ready for QA

UI: Displays 5 status columns:
- Developing
- Testing
- Under Review
- Done
- Ready for QA

✅ The UI matches the database! All 5 statuses from the database 
are displayed in the UI.

However, the expected test statuses only include 4 statuses 
(Developing, Under Review, Testing, Done), which means "Ready for QA" 
is an unexpected status that will cause test failures.
```

## What the LLM Can Detect

✅ **Missing UI elements** - Data in DB but not in UI
✅ **Extra UI elements** - Data in UI but not in DB
✅ **Status mismatches** - Different statuses between DB and UI
✅ **Count discrepancies** - Different number of items
✅ **Structural issues** - UI layout problems
✅ **Data inconsistencies** - Any mismatch between sources

## Technical Details

### Accessibility Snapshot Structure:
```json
{
  "role": "WebArea",
  "name": "Agile Storyboard",
  "children": [
    {
      "role": "heading",
      "name": "Developing",
      "level": 3
    },
    ...
  ]
}
```

The LLM extracts status columns by finding all `heading` elements with `level: 3`.

### What Gets Sent to the LLM:

1. **Database data** - Full JSON of all assignments
2. **UI status columns** - Extracted from accessibility tree
3. **Full accessibility tree** - Truncated to 2000 chars
4. **HTML availability** - Note that HTML is available

This gives the LLM complete context to compare and analyze!

## Benefits

🎯 **Automated QA** - LLM finds discrepancies automatically
🎯 **Natural Language** - Ask questions in plain English
🎯 **Multi-source Analysis** - Compares DB, UI structure, and rendered HTML
🎯 **Real-time** - Always uses current data
🎯 **Comprehensive** - Sees everything a QA engineer would see

---

**Try it now!** Run `python3 llm_client.py` and ask: "Does the UI match the database?"

