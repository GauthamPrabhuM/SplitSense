#!/bin/bash
# Quick script to check OAuth setup

echo "🔍 Checking OAuth Setup..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "📝 Create .env file with:"
    echo "   SPLITWISE_CLIENT_ID=your_client_id"
    echo "   SPLITWISE_CLIENT_SECRET=your_client_secret"
    echo "   SPLITWISE_REDIRECT_URI=http://localhost:8000/auth/callback"
    echo ""
    echo "Get credentials from: https://secure.splitwise.com/apps"
    exit 1
fi

# Load .env
export $(cat .env | grep -v '^#' | xargs)

# Check variables
if [ -z "$SPLITWISE_CLIENT_ID" ]; then
    echo "❌ SPLITWISE_CLIENT_ID not set in .env"
    exit 1
fi

if [ -z "$SPLITWISE_CLIENT_SECRET" ]; then
    echo "❌ SPLITWISE_CLIENT_SECRET not set in .env"
    exit 1
fi

# Test Python import
source venv/bin/activate
python -c "from auth.oauth import SplitwiseOAuth; oauth = SplitwiseOAuth(); print('✅ OAuth configured correctly!')" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Everything looks good! OAuth should work now."
    echo ""
    echo "🚀 Start server with:"
    echo "   uvicorn main:app --reload"
    echo ""
    echo "Then open: http://localhost:8000"
else
    echo ""
    echo "❌ OAuth configuration error. Check your .env file."
fi

