#!/bin/bash

echo "========================================="
echo "🚀 AQUAMITRA - Full Stack Startup"
echo "========================================="
echo ""

# Check if backend is ready
echo "📋 Checking backend requirements..."
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: /usr/local/bin/python3.11 -m venv .venv"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    exit 1
fi

if [ ! -d "data/ingres" ]; then
    echo "❌ Data directory not found!"
    exit 1
fi

echo "✅ Backend ready"
echo ""

# Check if frontend is ready
echo "📋 Checking frontend requirements..."
if [ ! -d "chatbot-ui/node_modules" ]; then
    echo "❌ Frontend dependencies not installed!"
    echo "   Run: cd chatbot-ui && npm install"
    exit 1
fi

echo "✅ Frontend ready"
echo ""

echo "========================================="
echo "🚀 Starting Services"
echo "========================================="
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "🐍 Starting Backend Server (Port 8000)..."
source .venv/bin/activate
python server.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Check if backend is running
if ! curl -s http://localhost:8000/api/health > /dev/null; then
    echo "❌ Backend failed to start! Check backend.log"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend running on http://localhost:8000"
echo ""

# Start frontend
echo "⚛️  Starting Frontend (Port 5173)..."
cd chatbot-ui
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 5

echo "✅ Frontend running on http://localhost:5173"
echo ""

echo "========================================="
echo "✅ ALL SERVICES RUNNING"
echo "========================================="
echo ""
echo "📍 Frontend UI:  http://localhost:5173"
echo "📍 Backend API:  http://localhost:8000"
echo "📍 API Docs:     http://localhost:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Keep script running
wait

