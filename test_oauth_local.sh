#!/bin/bash
# Script to test OAuth locally

echo "🔐 Testing OAuth Setup for SplitSense"
echo "======================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Creating .env.example template..."
    cat > .env.example << EOF
# Splitwise OAuth Configuration
SPLITWISE_CLIENT_ID=your_client_id_here
SPLITWISE_CLIENT_SECRET=your_client_secret_here
SPLITWISE_REDIRECT_URI=http://localhost:8000/auth/callback
EOF
    echo "✅ Created .env.example"
    echo ""
    echo "📝 Please create a .env file with your OAuth credentials:"
    echo "   1. Go to https://secure.splitwise.com/apps"
    echo "   2. Create a new app (Web Application type)"
    echo "   3. Set Redirect URI to: http://localhost:8000/auth/callback"
    echo "   4. Copy Client ID and Client Secret"
    echo "   5. Create .env file with:"
    echo "      SPLITWISE_CLIENT_ID=your_client_id"
    echo "      SPLITWISE_CLIENT_SECRET=your_client_secret"
    echo "      SPLITWISE_REDIRECT_URI=http://localhost:8000/auth/callback"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if required variables are set
if [ -z "$SPLITWISE_CLIENT_ID" ] || [ -z "$SPLITWISE_CLIENT_SECRET" ]; then
    echo "❌ Missing OAuth credentials in .env file!"
    echo "   Required: SPLITWISE_CLIENT_ID, SPLITWISE_CLIENT_SECRET"
    exit 1
fi

echo "✅ OAuth credentials found"
echo ""
echo "🚀 Starting server..."
echo "   Open http://localhost:8000 in your browser"
echo "   Click 'Connect with Splitwise' to test OAuth"
echo ""

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

