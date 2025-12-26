# Vercel Setup Instructions

## Important: Root Directory Configuration

Vercel needs to know that your Next.js app is in the `frontend/` directory.

## Option 1: Configure in Vercel Dashboard (Recommended)

1. Go to your Vercel project dashboard
2. Click **Settings** → **General**
3. Find **Root Directory**
4. Click **Edit**
5. Set to: `frontend`
6. Click **Save**

This tells Vercel to:
- Look for `package.json` in `frontend/` directory
- Run build commands from `frontend/` directory
- Use `frontend/.next` as output directory

## Option 2: Use vercel.json (Alternative)

The `vercel.json` file is configured, but you still need to set Root Directory in dashboard to `frontend`.

## After Setting Root Directory

1. Go to **Deployments** tab
2. Click **Redeploy** on the latest deployment
3. Or push a new commit to trigger auto-deploy

## Verify Build

Check the build logs - you should see:
```
✓ Installing dependencies
✓ Building Next.js app
✓ Build completed
```

## Troubleshooting

### Still getting "No Next.js version detected"

1. **Check Root Directory**: Must be set to `frontend` in Vercel dashboard
2. **Check package.json**: Should be at `frontend/package.json`
3. **Check next version**: Should be in `frontend/package.json` dependencies

### Build fails

1. Check build logs in Vercel dashboard
2. Verify `frontend/package.json` has `next` in dependencies
3. Check Node.js version (should be 18+)

## Quick Fix

1. Vercel Dashboard → Settings → General
2. Root Directory → Edit → Set to `frontend`
3. Save
4. Redeploy

That's it! 🎉

