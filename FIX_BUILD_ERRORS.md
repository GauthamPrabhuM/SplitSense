# Fix Build Errors - Render & Vercel

## Render Error: Python 3.13 Compatibility

### Problem
Render is using Python 3.13.4, but `pandas==2.1.3` doesn't support Python 3.13 (requires Python 3.9-3.12).

### Solution
Created `runtime.txt` and updated `render.yaml` to use Python 3.11.9.

## Vercel Error: Frontend Directory

### Problem  
Build command trying to `cd frontend` but directory not found.

### Solution
Root `vercel.json` is configured correctly. If still failing, check:
1. Root Directory is NOT set in Vercel dashboard (should be root `/`)
2. The `vercel.json` file is in the root directory

## Files Changed

1. **`runtime.txt`** - Specifies Python 3.11.9
2. **`render.yaml`** - Added `pythonVersion: "3.11.9"`
3. **`vercel.json`** - Root-level config with correct build commands

## Next Steps

1. **Commit and push**:
   ```bash
   git add runtime.txt render.yaml vercel.json
   git commit -m "Fix Python version for Render and Vercel build config"
   git push
   ```

2. **Redeploy on Render**:
   - Render will auto-detect `runtime.txt` and use Python 3.11
   - Or manually set Python version in Render dashboard: **Settings** → **Python Version** → `3.11.9`

3. **Redeploy on Vercel**:
   - Should auto-deploy on push
   - Or manually redeploy in Vercel dashboard

## Verify

- Render: Check build logs for "Using Python version 3.11.9"
- Vercel: Check build logs for successful Next.js build

Both should now build successfully! 🎉

