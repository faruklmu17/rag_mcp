# mcp_server.py
import aiosqlite
import json
import os
from fastmcp import FastMCP
from typing import List, Dict

mcp = FastMCP("Agile QA MCP Server")
DB_PATH = "db/agile_board.db"
SNAPSHOT_DIR = "snapshots"

@mcp.resource("assignments://all")
async def get_assignments() -> List[Dict]:
    """Get all assignments from the database"""
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("""
            SELECT a.id, e.name as engineer, w.title as work_item, a.status
            FROM assignments a
            JOIN engineers e ON a.engineer_id = e.id
            JOIN work_items w ON a.work_item_id = w.id
        """)
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) async for row in cursor]
        await cursor.close()
    return rows

@mcp.resource("ui://snapshot/accessibility")
async def get_ui_accessibility_snapshot() -> Dict:
    """Get the UI accessibility tree snapshot"""
    snapshot_path = os.path.join(SNAPSHOT_DIR, "ui_snapshot.json")
    if not os.path.exists(snapshot_path):
        return {"error": "Snapshot not found. Run: npx playwright test scripts/snapshot_accessibility.spec.ts"}

    with open(snapshot_path, 'r') as f:
        return json.load(f)

@mcp.resource("ui://snapshot/html")
async def get_ui_html_snapshot() -> str:
    """Get the UI HTML DOM snapshot"""
    snapshot_path = os.path.join(SNAPSHOT_DIR, "ui_snapshot.html")
    if not os.path.exists(snapshot_path):
        return "Error: Snapshot not found. Run: npx playwright test scripts/snapshot_dom.spec.ts"

    with open(snapshot_path, 'r') as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(transport="stdio")
