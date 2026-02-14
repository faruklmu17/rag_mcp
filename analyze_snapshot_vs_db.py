import sqlite3
import json
import sys

# -- Inputs --
SNAPSHOT_FILE = sys.argv[1] if len(sys.argv) > 1 else 'snapshots/ui_snapshot.json'
DB_PATH = sys.argv[2] if len(sys.argv) > 2 else 'db/agile_board.db'

# -- From Tests --
expected_statuses = {'Developing', 'Under Review', 'Testing', 'Done'}

# -- From UI Snapshot --
with open(SNAPSHOT_FILE, 'r') as f:
    snapshot = json.load(f)

snapshot_statuses = {
    node['name'] for node in snapshot.get("children", [])
    if node.get("role") == "heading" and node.get("level") == 3
}

# -- From DB --
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT DISTINCT status FROM assignments")
db_statuses = {row[0] for row in cursor.fetchall()}
conn.close()

# -- Tests --
print("\n🧪 UI Snapshot Test Summary\n" + "-"*35)

# 1. UI column count
if len(snapshot_statuses) == len(expected_statuses):
    print(f"✅ Test 1: UI column count is correct ({len(snapshot_statuses)})")
else:
    print(f"❌ Test 1: UI shows {len(snapshot_statuses)} columns, expected {len(expected_statuses)}")

# 2. UI contains only expected columns
unexpected = snapshot_statuses - expected_statuses
if unexpected:
    print(f"❌ Test 2: UI has unexpected columns: {', '.join(unexpected)}")
else:
    print("✅ Test 2: UI only shows expected statuses")

# 3. DB has statuses not shown in UI
missing_in_ui = db_statuses - snapshot_statuses
if missing_in_ui:
    print(f"❌ Test 3: UI is missing statuses from DB: {', '.join(missing_in_ui)}")
else:
    print("✅ Test 3: All DB statuses are visible in the UI")

# 4. DB has statuses missing from tests
missing_from_tests = db_statuses - expected_statuses
if missing_from_tests:
    print(f"⚠️  Warning: Test assertions do not account for: {', '.join(missing_from_tests)}")
else:
    print("✅ Test 4: All DB statuses are covered by tests")
