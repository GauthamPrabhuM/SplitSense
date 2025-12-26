# Fix: Vercel Can't Find Frontend Directory

## Problem
```
cd: frontend: No such file or directory
```

This means Vercel is building from the root, but the build command tries to `cd frontend`.

## Solution: Set Root Directory in Vercel Dashboard

You **MUST** set Root Directory to `frontend` in the Vercel dashboard. Here's how:

### Step-by-Step Instructions

1. Go to your Vercel project dashboard
2. Click **Settings** (top navigation)
3. Scroll down to **General** section
4. Find **Root Directory**
5. Click the **Edit** button (pencil icon) next to it
6. In the input field, type: `frontend`
7. Click **Save**

### After Setting Root Directory

Once Root Directory is set to `frontend`, you can simplify `vercel.json`:

**Delete the root `vercel.json`** and create `frontend/vercel.json`:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://splitsense.onrender.com/api/:path*"
    },
    {
      "source": "/auth/:path*",
      "destination": "https://splitsense.onrender.com/auth/:path*"
    }
  ]
}
```

This way:
- ✅ Vercel builds from `frontend/` directory directly
- ✅ No need for `cd frontend` commands
- ✅ TypeScript paths resolve correctly
- ✅ Next.js auto-detection works perfectly

### If You Still Can't Edit Root Directory

Try these alternatives:

1. **Delete and Re-import Project**:
   - Delete the current Vercel project
   - Create a new project
   - When importing, look for "Configure Project" or "Advanced" options
   - Set Root Directory to `frontend` before first deploy

2. **Use Vercel CLI** (bypasses dashboard):
   ```bash
   cd frontend
   npm install -g vercel
   vercel login
   vercel --prod
   ```
   This deploys from the frontend directory directly, no Root Directory setting needed.

### Why Root Directory is Required

Vercel needs to know:
- Where your `package.json` is located
- Where to run build commands
- Where TypeScript config files are

Setting Root Directory to `frontend` tells Vercel: "Everything is in the frontend/ subdirectory."

## Quick Fix Checklist

- [ ] Go to Vercel dashboard → Settings → General
- [ ] Find "Root Directory"
- [ ] Click Edit
- [ ] Set to: `frontend`
- [ ] Save
- [ ] Delete root `vercel.json`
- [ ] Create `frontend/vercel.json` with rewrites only
- [ ] Redeploy

This is the standard way to deploy Next.js apps in subdirectories on Vercel! 🎯

