# SplitSense 💰

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

A comprehensive, **secure** analytics platform for Splitwise with real-time insights, beautiful visualizations, and OAuth authentication.

🔗 **Live Demo**: [https://splitsense.onrender.com](https://splitsense.onrender.com)

---

## ✨ Features

### Analytics & Insights
- **Spending Analysis**: Monthly, quarterly, and yearly spending trends with peak detection
- **Balance Tracking**: Real-time balances with friends using Splitwise API
- **Category Breakdown**: Visualize spending by category with pie charts
- **Group Insights**: Analyze spending patterns across different groups
- **Friction Analysis**: Identify settlement bottlenecks and slow-paying friends
- **Anomaly Detection**: Automatically flag unusual transactions
- **Subscription Detection**: Identify recurring expenses
- **Balance Predictions**: AI-powered balance forecasting

### Modern UI
- **Next.js 14 Dashboard**: Beautiful, responsive React frontend
- **Interactive Charts**: Powered by Recharts for smooth visualizations
- **Dark Mode Support**: Automatic theme detection
- **PDF Reports**: Generate newspaper-style analytics reports

### Security
- **OAuth 2.0 Authentication**: Secure login via Splitwise
- **Session-Based Auth**: HTTPOnly cookies with signed session tokens
- **User Data Isolation**: Each user only sees their own data
- **Rate Limiting**: Per-user API rate limiting
- **CORS Protection**: Configurable allowed origins

---

## 🚀 Quick Start

### Option 1: Deploy to Render (Recommended)

1. Fork this repository
2. Create a [Splitwise App](https://secure.splitwise.com/apps) to get OAuth credentials
3. Deploy to [Render](https://render.com) using the `render.yaml` blueprint
4. Set environment variables in Render dashboard (see below)

### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/GauthamPrabhuM/SplitSense.git
cd SplitSense

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Splitwise OAuth credentials

# Run the backend
uvicorn main:app --reload --port 8000

# In another terminal, run the frontend
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` for the frontend dashboard.

---

## 🔐 Environment Variables

### Required for OAuth

| Variable | Description | Example |
|----------|-------------|---------|
| `SPLITWISE_CLIENT_ID` | Your Splitwise app client ID | `0QX3DGCz...` |
| `SPLITWISE_CLIENT_SECRET` | Your Splitwise app client secret | `j89620...` |
| `SPLITWISE_REDIRECT_URI` | OAuth callback URL | `https://yourapp.com/auth/callback` |
| `SESSION_SECRET_KEY` | Secret for signing session cookies | Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |

### Optional Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `FRONTEND_URL` | URL for frontend redirects | `http://localhost:3000` |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:3000,http://localhost:8000` |
| `ENVIRONMENT` | `development` or `production` | `development` |
| `BASE_CURRENCY` | Default currency for display | `USD` |
| `MASK_SENSITIVE_DATA` | Mask sensitive data in logs | `false` |

---

## 📡 API Reference

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/auth/login` | Initiate Splitwise OAuth login | ❌ |
| `GET` | `/auth/callback` | OAuth callback (handles redirect) | ❌ |
| `POST` | `/auth/logout` | Log out current user | ✅ |
| `GET` | `/api/me` | Get current user info | ✅ |

### Data Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/health` | Health check | ❌ |
| `POST` | `/api/refresh` | Refresh data from Splitwise | ✅ |
| `GET` | `/api/insights` | Get all analytics insights | ✅ |
| `GET` | `/api/friends` | Get friend balances | ✅ |
| `GET` | `/api/report` | Download PDF analytics report | ✅ |
| `GET` | `/api/export/csv` | Export insights as CSV | ✅ |
| `GET` | `/api/export/pdf` | Export insights as PDF | ✅ |

### Legacy Endpoints (Development Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/ingest` | Ingest data via API token |
| `POST` | `/api/ingest/file` | Ingest data from file upload |

---

## 🏗️ Architecture

```
SplitSense/
├── main.py                     # FastAPI application entry point
├── auth/                       # Authentication module
│   ├── oauth.py               # Splitwise OAuth 2.0 client
│   ├── sessions.py            # Session management (user-scoped storage)
│   └── middleware.py          # Auth dependencies & middleware
├── ingestion/                  # Data ingestion layer
│   ├── api_client.py          # Splitwise API client
│   ├── file_parser.py         # CSV/JSON parser
│   └── normalizer.py          # Currency/timestamp normalization
├── analytics/                  # Analytics engine
│   ├── spending.py            # Spending analysis
│   ├── balances.py            # Balance analysis
│   ├── categories.py          # Category analysis
│   ├── groups.py              # Group analysis
│   ├── advanced.py            # Anomalies, subscriptions, predictions
│   └── report_generator.py    # PDF report generation
├── models/                     # Data models
│   └── schemas.py             # Pydantic models
├── validation/                 # Data integrity checks
│   └── verifier.py            # Cross-verification logic
├── visualization/              # Chart generation
│   └── charts.py              # Plotly visualizations
├── frontend/                   # Next.js 14 frontend
│   ├── src/
│   │   ├── app/               # App router pages
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities & API hooks
│   │   └── types/             # TypeScript types
│   └── package.json
├── Dockerfile                  # Multi-stage Docker build
├── render.yaml                 # Render deployment config
└── requirements.txt            # Python dependencies
```

---

## 🔒 Security Model

### Session-Based Authentication

1. **User logs in** via Splitwise OAuth
2. **Server creates session** with signed, HTTPOnly cookie
3. **User data stored in session** (isolated from other users)
4. **API requests validated** via session cookie
5. **Session expires** after 24 hours of inactivity

### Security Features

| Feature | Implementation |
|---------|----------------|
| **Session Cookies** | HTTPOnly, Secure (HTTPS), SameSite=Lax |
| **Session Signing** | HMAC-SHA256 with `SESSION_SECRET_KEY` |
| **Data Isolation** | User data keyed by session ID, not shared |
| **CSRF Protection** | OAuth state parameter validation |
| **Rate Limiting** | Per-user limits via slowapi |
| **CORS** | Configurable allowed origins |

### What This Prevents

- ✅ Cross-user data access
- ✅ Session hijacking (HTTPOnly cookies)
- ✅ CSRF attacks (SameSite + OAuth state)
- ✅ Token leakage (no tokens in localStorage)
- ✅ URL manipulation attacks

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=. --cov-report=html
```

---

## 📊 Data Validation

The tool performs these correctness checks:

1. **Balance Verification**: Sum of all group balances equals zero
2. **Expense Totals**: Paid amounts equal owed amounts per expense
3. **Net Balance**: Personal balance matches sum of group balances
4. **Settlement Integrity**: Settlements balance to zero
5. **Currency Consistency**: Amounts in a group use the same currency

---

## 🌐 Deployment

### Render (Recommended)

The `render.yaml` includes full deployment config:

```yaml
services:
  - type: web
    name: splitsense
    env: docker
    plan: free
    healthCheckPath: /api/health
```

Set these secrets in Render dashboard:
- `SPLITWISE_CLIENT_ID`
- `SPLITWISE_CLIENT_SECRET`
- `SESSION_SECRET_KEY`

### Docker

```bash
# Build
docker build -t splitsense .

# Run
docker run -p 8000:8000 \
  -e SPLITWISE_CLIENT_ID=... \
  -e SPLITWISE_CLIENT_SECRET=... \
  -e SESSION_SECRET_KEY=... \
  splitsense
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- [Splitwise](https://www.splitwise.com/) for the amazing expense-sharing platform
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python web framework
- [Next.js](https://nextjs.org/) for the React framework
- [Tailwind CSS](https://tailwindcss.com/) for styling
- [Recharts](https://recharts.org/) for chart components

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/GauthamPrabhuM">Gautham Prabhu M</a>
  <br>
  <a href="https://buymeacoffee.com/gauthamprabhum">☕ Buy me a coffee</a>
</p>

