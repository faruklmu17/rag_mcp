#!/bin/bash
# Generate UI snapshots for MCP server

echo "📸 Generating UI Snapshots..."
echo ""

# Check if the HTML file is being served
echo "⚠️  Make sure index.html is being served at http://127.0.0.1:5500/index.html"
echo "   (Use Live Server in VS Code or run: python3 -m http.server 5500)"
echo ""
read -p "Press Enter when the server is running, or Ctrl+C to cancel..."

echo ""
echo "Generating accessibility snapshot..."
npx playwright test scripts/snapshot_accessibility.spec.ts

echo ""
echo "Generating DOM HTML snapshot..."
npx playwright test scripts/snapshot_dom.spec.ts

echo ""
echo "✅ Snapshots generated!"
echo ""
echo "Generated files:"
ls -lh snapshots/
echo ""
echo "Now you can run: python3 llm_client.py"

