#!/bin/bash

echo "========================================="
echo "🚀 AQUAMITRA - Groundwater Data Assistant"
echo "========================================="
echo ""

# Check data files
echo "📁 Checking data files..."
if [ -d "data/ingres" ]; then
    echo "✅ Data directory exists"
    echo "   Files: $(ls data/ingres/*.csv 2>/dev/null | wc -l | tr -d ' ') CSV files found"
else
    echo "❌ Data directory not found!"
    exit 1
fi

echo ""

# Check environment
echo "🔑 Checking environment..."
if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    echo "❌ .env file not found!"
    exit 1
fi

echo ""

# Check virtual environment
echo "🐍 Checking Python environment..."
if [ -d ".venv" ]; then
    echo "✅ Virtual environment exists"
    source .venv/bin/activate
    echo "   Python: $(python --version)"
else
    echo "❌ Virtual environment not found!"
    echo "   Run: /usr/local/bin/python3.11 -m venv .venv"
    exit 1
fi

echo ""
echo "========================================="
echo "🚀 Starting FastAPI Server"
echo "========================================="
echo ""
echo "📍 Server will run on: http://localhost:8000"
echo "📍 API Documentation: http://localhost:8000/docs"
echo "📍 Health Check: http://localhost:8000/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "========================================="
echo ""

# Start the server
python server.py

