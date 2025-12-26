#!/bin/bash
# Run both frontend and backend together

cd "$(dirname "$0")"

echo "🚀 Starting SplitSense Full Stack..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please update it with your OAuth credentials."
    fi
fi

# Activate Python virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Python virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Check backend dependencies
if ! python -c "import fastapi" 2>/dev/null; then
    echo "⚠️  Backend dependencies not installed. Installing..."
    pip install -r requirements.txt
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Frontend dependencies not installed. Installing..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "📦 Starting services..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start backend
echo "🔧 Starting Backend (FastAPI) on http://localhost:8000"
source venv/bin/activate
export $(cat .env | grep -v '^#' | xargs 2>/dev/null)
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > /tmp/splitsense_backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "⏳ Waiting for backend to start..."
for i in {1..10}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    sleep 1
done

# Start frontend
echo "⚛️  Starting Frontend (Next.js) on http://localhost:3000"
cd frontend
npm run dev > /tmp/splitsense_frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Services started!"
echo ""
echo "📊 Backend API:  http://localhost:8000"
echo "📚 API Docs:     http://localhost:8000/docs"
echo "🎨 Frontend:     http://localhost:3000"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f /tmp/splitsense_backend.log"
echo "   Frontend: tail -f /tmp/splitsense_frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for both processes
wait

