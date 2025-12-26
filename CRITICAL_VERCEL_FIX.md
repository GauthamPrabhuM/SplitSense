# ⚠️ CRITICAL: You MUST Set Root Directory in Vercel Dashboard

## The Problem

Vercel can't find the `frontend` directory because Root Directory isn't set.

## The Solution (REQUIRED)

You **MUST** set Root Directory in Vercel dashboard - there's no way around it when using GitHub integration.

### How to Set Root Directory

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard
2. **Click your project**
3. **Click "Settings"** (top navigation)
4. **Scroll to "General"** section
5. **Find "Root Directory"**
6. **Click "Edit"** (pencil icon)
7. **Type**: `frontend`
8. **Click "Save"**
9. **Redeploy**

## Files Changed

I've:
- ✅ **Deleted** root `vercel.json` (not needed when Root Directory is set)
- ✅ **Created** `frontend/vercel.json` (only rewrites, no build commands)

## After Setting Root Directory

1. Vercel will automatically:
   - Look for `package.json` in `frontend/`
   - Run `npm install` in `frontend/`
   - Run `npm run build` in `frontend/`
   - Use `frontend/.next` as output

2. No build commands needed in `vercel.json` - Vercel auto-detects Next.js

## If You Still Can't Edit It

**Option 1: Delete and Re-import**
- Delete current project in Vercel
- Create new project
- When importing, set Root Directory BEFORE first deploy

**Option 2: Use Vercel CLI** (no dashboard needed)
```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

## Why This is Required

Vercel's GitHub integration requires Root Directory to be set for monorepos/subdirectory deployments. This is by design and cannot be bypassed via configuration files alone.

**Set Root Directory = `frontend` → Problem solved!** ✅

