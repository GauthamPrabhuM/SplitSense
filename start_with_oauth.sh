#!/bin/bash
# Start server with OAuth support

echo "🚀 Starting SplitSense with OAuth..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Load environment variables from .env
export $(cat .env | grep -v '^#' | xargs)

# Check if OAuth is configured
python -c "from auth.oauth import SplitwiseOAuth; oauth = SplitwiseOAuth(); print('✅ OAuth configured!')" 2>&1

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ OAuth not configured. Check your .env file."
    exit 1
fi

echo ""
echo "🌐 Server starting..."
echo "   Open: http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""

# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

