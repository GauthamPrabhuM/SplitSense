# Fix Vercel Path Alias Error

## Problem
Vercel build failing with:
```
Module not found: Can't resolve '@/lib/api'
Module not found: Can't resolve '@/lib/utils'
```

## Root Cause
TypeScript path aliases (`@/*`) aren't being resolved correctly during Vercel build.

## Solution Applied

1. ✅ Updated `tsconfig.json` - Added `rootDir` for clarity
2. ✅ Updated `vercel.json` - Set `framework: "nextjs"` (was `null`)

## Files Changed

- `frontend/tsconfig.json` - Added `rootDir: "."`
- `vercel.json` - Changed `framework: null` to `framework: "nextjs"`

## Why This Works

- `framework: "nextjs"` tells Vercel to use Next.js-specific build optimizations
- Next.js will properly resolve TypeScript path aliases from `tsconfig.json`
- The `rootDir` ensures TypeScript knows the correct base directory

## Next Steps

1. **Commit and push**:
   ```bash
   git add frontend/tsconfig.json vercel.json
   git commit -m "Fix TypeScript path alias resolution in Vercel"
   git push
   ```

2. **Redeploy**: Vercel will auto-deploy on push

The build should now succeed! 🎉

