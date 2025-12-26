# Alternative Fix: Set Root Directory in Vercel Dashboard

## If Build Still Fails

The best solution is to set **Root Directory** to `frontend` in Vercel dashboard:

1. Go to Vercel project dashboard
2. **Settings** → **General**
3. Find **Root Directory**
4. Click **Edit**
5. Set to: `frontend`
6. Click **Save**
7. Remove the root `vercel.json` file
8. Create `frontend/vercel.json` instead:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://splitsense-backend.onrender.com/api/:path*"
    },
    {
      "source": "/auth/:path*",
      "destination": "https://splitsense-backend.onrender.com/auth/:path*"
    }
  ]
}
```

This way:
- Vercel builds from `frontend/` directory directly
- No need for `cd frontend` commands
- TypeScript paths resolve correctly
- Next.js auto-detection works perfectly

## Current Fix (Without Dashboard Changes)

The current `vercel.json` should work with `framework: "nextjs"`. If it still fails, try the dashboard approach above.

