# Agile QA MCP Server

A demonstration project showcasing automated quality assurance testing for an agile storyboard application using **Model Context Protocol (MCP)**, **Playwright**, and **snapshot-based testing**.

## 🎯 Purpose

This project demonstrates how to catch UI bugs by comparing what the database contains versus what the UI actually displays. It intentionally includes a discrepancy (a "Ready for QA" status) to showcase automated testing techniques that can detect such issues.

## 🏗️ Architecture

### Components

1. **Frontend (`index.html`)**
   - Simple agile storyboard UI displaying work items across status columns
   - Dynamically renders columns based on assignment data
   - Shows engineer assignments and work items

2. **Backend (`mcp_server.py`)**
   - FastMCP server exposing data via MCP resources
   - Connects to SQLite database
   - Provides three resource endpoints:
     - `assignments://all` - Database assignments
     - `ui://snapshot/accessibility` - UI accessibility tree
     - `ui://snapshot/html` - UI HTML DOM

3. **Database (`init_db.py`)**
   - SQLite database with three tables:
     - `engineers` - Developer and QA team members
     - `work_items` - Stories and Defects
     - `assignments` - Links engineers to work items with status
   - Seeded with sample data including the intentional "Ready for QA" status

4. **Testing Infrastructure**
   - **Playwright** - Browser automation and UI testing
   - **Snapshot Testing** - Captures DOM HTML and accessibility tree
   - **Analysis Script** - Compares UI snapshots against database state

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Node.js 14+ (for Playwright tests)
- Groq API Key (get one at https://console.groq.com/keys)

### Quick Setup

Run the automated setup script:
```bash
./setup_llm.sh
```

Or follow manual installation steps below.

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag_mcp
   ```

2. **Install Python dependencies**
   ```bash
   pip install fastmcp aiosqlite httpx mcp python-dotenv
   ```

3. **Install Node.js dependencies (for testing)**
   ```bash
   npm install
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Install Playwright browsers (optional, for testing)**
   ```bash
   npx playwright install
   ```

### Running the LLM + MCP Integration

**Setup your API key:**

1. Copy the example env file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your-actual-api-key-here
   ```
   Get your key from: https://console.groq.com/keys

**Query the agile board using AI:**

```bash
python3 llm_client.py
```

You can ask questions like:

**Database queries:**
- "What assignments does Alice Smith have?"
- "Which work items are in Testing status?"
- "Are there any items in Ready for QA status?"
- "Summarize the current state of the agile board"
- "Which engineers are working on defects?"

**UI analysis:**
- "What status columns are shown in the UI?"
- "Does the UI match the database?"
- "Are there any discrepancies between the DB and UI?"
- "Compare database statuses with UI columns"

See `DOM_ANALYSIS_GUIDE.md` for more details on UI + Database analysis.

### Running the Frontend (Optional)

1. **Serve the frontend**
   - Use any local web server (e.g., Live Server in VS Code, Python's http.server, etc.)
   - Default URL: `http://127.0.0.1:5500/index.html`

## 🧪 Testing

### Run Playwright Tests

```bash
npx playwright test
```

### View Test Report

```bash
npx playwright show-report
```

### Generate UI Snapshots

The project includes scripts to capture UI snapshots:

- **DOM Snapshot**: `scripts/snapshot_dom.spec.ts`
- **Accessibility Snapshot**: `scripts/snapshot_accessibility.spec.ts`

Run snapshot generation:
```bash
npx playwright test scripts/snapshot_accessibility.spec.ts
```

### Analyze Snapshot vs Database

Compare UI snapshot against database state:

```bash
python analyze_snapshot_vs_db.py
```

This will output a test summary showing:
- ✅ UI column count validation
- ❌ Unexpected columns in UI
- ❌ Missing statuses from DB
- ⚠️ Test coverage gaps

## 🐛 Intentional Bug

The project includes an intentional discrepancy to demonstrate testing capabilities:

- **Database** includes a "Ready for QA" status (line 69 in `init_db.py`)
- **UI** displays this status dynamically (line 73 in `index.html`)
- **Tests** expect only 4 statuses: Developing, Under Review, Testing, Done
- **Result**: Tests fail, revealing the UI/DB mismatch

## 📊 Database Schema

```sql
engineers (id, name, role)
work_items (id, title, type)
assignments (id, engineer_id, work_item_id, status)
```

**Allowed Statuses**: Developing, Under Review, Testing, Done, Ready for QA

## 🛠️ Technologies

- **FastMCP** - Model Context Protocol server framework
- **Playwright** - End-to-end testing framework
- **SQLite** - Lightweight database
- **TypeScript** - Test scripting
- **Python** - Backend and database management

## 📝 Key Files

- `llm_client.py` - **LLM client that connects Groq to MCP server (DB + UI analysis)**
- `mcp_server.py` - MCP server exposing database + UI snapshots
- `init_db.py` - Database initialization and seeding
- `index.html` - Frontend storyboard UI
- `tests/storyboard.spec.ts` - Playwright test suite
- `analyze_snapshot_vs_db.py` - Snapshot analysis script
- `setup_llm.sh` - Automated setup script
- `generate_snapshots.sh` - Generate UI snapshots for MCP
- `DOM_ANALYSIS_GUIDE.md` - Guide for UI + Database analysis
- `playwright.config.ts` - Playwright configuration

## 🎓 Learning Outcomes

This project demonstrates:
- Setting up an MCP server with FastMCP
- Browser automation with Playwright
- Snapshot-based testing techniques
- Comparing UI state against database state
- Detecting UI/data discrepancies automatically
- Agile workflow visualization

## 📄 License

ISC

## 👥 Contributors

Open for contributions! Feel free to submit issues and pull requests.