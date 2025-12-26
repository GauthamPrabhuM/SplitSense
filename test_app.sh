#!/bin/bash
# Test the full stack application

echo "🧪 Testing SplitSense Application"
echo "================================="
echo ""

# Check if services are running
echo "1️⃣ Checking Backend..."
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "   ✅ Backend is running"
    curl -s http://localhost:8000/api/health | python3 -m json.tool
else
    echo "   ❌ Backend is not running"
    echo "   Start it with: ./run_full_stack.sh"
    exit 1
fi

echo ""
echo "2️⃣ Checking Frontend..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "   ✅ Frontend is running"
else
    echo "   ❌ Frontend is not running"
    echo "   Start it with: ./run_full_stack.sh"
    exit 1
fi

echo ""
echo "3️⃣ Testing API Endpoints..."

# Test health
echo "   Testing /api/health..."
HEALTH=$(curl -s http://localhost:8000/api/health)
if echo "$HEALTH" | grep -q "healthy"; then
    echo "   ✅ Health check passed"
else
    echo "   ❌ Health check failed"
fi

# Test OAuth availability
echo "   Testing OAuth availability..."
OAUTH_AVAILABLE=$(echo "$HEALTH" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('oauth_available', False))" 2>/dev/null)
if [ "$OAUTH_AVAILABLE" = "True" ]; then
    echo "   ✅ OAuth is configured"
else
    echo "   ⚠️  OAuth is not configured (manual tokens still work)"
fi

# Test insights endpoint (should fail if no data)
echo "   Testing /api/insights..."
INSIGHTS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/insights)
if [ "$INSIGHTS" = "404" ]; then
    echo "   ✅ Insights endpoint works (no data yet - expected)"
elif [ "$INSIGHTS" = "200" ]; then
    echo "   ✅ Insights endpoint works (data available)"
else
    echo "   ⚠️  Insights endpoint returned: $INSIGHTS"
fi

echo ""
echo "4️⃣ Testing OAuth Login..."
OAUTH_LOGIN=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/auth/login)
if [ "$OAUTH_LOGIN" = "200" ]; then
    echo "   ✅ OAuth login endpoint works"
    AUTH_URL=$(curl -s http://localhost:8000/auth/login | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('auth_url', 'N/A'))" 2>/dev/null)
    echo "   Auth URL: ${AUTH_URL:0:80}..."
else
    echo "   ⚠️  OAuth login endpoint returned: $OAUTH_LOGIN"
fi

echo ""
echo "✅ Testing complete!"
echo ""
echo "🌐 Access Points:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📝 Next Steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Click 'Connect with Splitwise' (if OAuth configured)"
echo "   3. Or use manual API token to ingest data"
echo "   4. View analytics dashboard"

