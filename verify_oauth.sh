#!/bin/bash
# Verify OAuth configuration

echo "🔍 Verifying OAuth Configuration..."
echo ""

# Check .env file
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    exit 1
fi

# Load .env
export $(cat .env | grep -v '^#' | xargs)

echo "📋 Current Configuration:"
echo "   CLIENT_ID: ${SPLITWISE_CLIENT_ID:0:20}..."
echo "   CLIENT_SECRET: ${SPLITWISE_CLIENT_SECRET:0:20}..."
echo "   REDIRECT_URI: $SPLITWISE_REDIRECT_URI"
echo ""

# Check if values are set
if [ -z "$SPLITWISE_CLIENT_ID" ]; then
    echo "❌ SPLITWISE_CLIENT_ID not set"
    exit 1
fi

if [ -z "$SPLITWISE_CLIENT_SECRET" ]; then
    echo "❌ SPLITWISE_CLIENT_SECRET not set"
    exit 1
fi

if [ -z "$SPLITWISE_REDIRECT_URI" ]; then
    echo "❌ SPLITWISE_REDIRECT_URI not set"
    exit 1
fi

echo "✅ All environment variables are set"
echo ""

# Check redirect URI format
if [[ "$SPLITWISE_REDIRECT_URI" != "http://localhost:8000/auth/callback" ]]; then
    echo "⚠️  WARNING: Redirect URI is: $SPLITWISE_REDIRECT_URI"
    echo "   Expected: http://localhost:8000/auth/callback"
    echo ""
    echo "   Make sure this EXACTLY matches your Splitwise app settings!"
    echo "   Go to: https://secure.splitwise.com/apps"
else
    echo "✅ Redirect URI is correct: $SPLITWISE_REDIRECT_URI"
fi

echo ""
echo "📝 Next Steps:"
echo "   1. Go to https://secure.splitwise.com/apps"
echo "   2. Open your app"
echo "   3. Verify Redirect URI matches: $SPLITWISE_REDIRECT_URI"
echo "   4. Make sure Application Type is 'Web Application'"
echo "   5. Restart your server and try again"
echo ""

