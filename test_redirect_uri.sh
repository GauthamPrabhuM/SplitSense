#!/bin/bash
# Test OAuth redirect URI configuration

echo "🔍 Testing OAuth Redirect URI Configuration"
echo "==========================================="
echo ""

# Load .env
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    exit 1
fi

export $(cat .env | grep -v '^#' | xargs)

REDIRECT_URI="$SPLITWISE_REDIRECT_URI"

echo "📋 Current Redirect URI: $REDIRECT_URI"
echo ""

# Check if server is running
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "⚠️  Server is not running on localhost:8000"
    echo "   Start server first: ./start_with_oauth.sh"
    echo ""
fi

# Test callback endpoint
echo "🧪 Testing callback endpoint..."
CALLBACK_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/auth/callback?code=test&state=test" 2>&1)

if [ "$CALLBACK_RESPONSE" = "400" ] || [ "$CALLBACK_RESPONSE" = "500" ]; then
    echo "✅ Callback endpoint is accessible (returned $CALLBACK_RESPONSE - expected for test)"
else
    echo "⚠️  Callback endpoint returned: $CALLBACK_RESPONSE"
fi

echo ""
echo "📝 IMPORTANT: Verify in Splitwise App Settings"
echo "   1. Go to: https://secure.splitwise.com/apps"
echo "   2. Open your app"
echo "   3. Check 'Redirect URI' field"
echo "   4. Must be EXACTLY: $REDIRECT_URI"
echo "   5. No trailing slash, exact match required!"
echo ""
echo "🔗 Test the auth URL:"
echo "   Run: curl http://localhost:8000/auth/login"
echo "   Then open the 'auth_url' in browser to test"
echo ""

