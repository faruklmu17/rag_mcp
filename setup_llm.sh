#!/bin/bash
# Setup script for LLM + MCP integration

echo "🚀 Setting up Agile Board QA Assistant..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install httpx mcp aiosqlite fastmcp python-dotenv

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python3 init_db.py

# Setup .env file
echo ""
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your Groq API key"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your Groq API key"
echo "     Get one at: https://console.groq.com/keys"
echo "  2. Run the LLM client:"
echo "     python3 llm_client.py"

