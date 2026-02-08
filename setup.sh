#!/bin/bash

echo "🚀 Setting up SIH 2025 SQL Coder..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your Google API key for multilingual support"
    echo "   Without it, only English will be supported."
    echo ""
fi

# Setup Python environment
echo "🐍 Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo ""
echo "📱 Setting up Frontend..."
cd chatbot-ui
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env and add your Google API key (optional, for multilingual support)"
echo "2. Start the backend: source .venv/bin/activate && python server.py"
echo "3. Start the frontend: cd chatbot-ui && npm run dev"
echo ""
echo "🌐 Backend will run on: http://localhost:8000"
echo "🌐 Frontend will run on: http://localhost:5173"
echo ""
echo "📚 For Google API key setup:"
echo "   - Go to https://console.cloud.google.com/"
echo "   - Enable 'Generative Language API'"
echo "   - Create an API key and add it to .env"
