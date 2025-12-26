# Deploy to Render (Free Tier)

This guide will help you deploy SplitSense to Render using their free tier.

## Quick Deploy

1. **Sign up/Login to Render**: https://render.com
   - Use GitHub to sign in (easiest)

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `GauthamPrabhuM/SplitSense`

3. **Configure the Service**:
   - **Name**: `splitsense` (or any name you prefer)
   - **Region**: Choose closest to you (Oregon, Frankfurt, Singapore, Mumbai)
   - **Branch**: `main` (or your deployment branch)
   - **Root Directory**: Leave empty (root of repo)
   - **Runtime**: Select "Docker"
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `.` (current directory)
   - **Start Command**: Leave empty (uses Dockerfile CMD)

4. **Environment Variables**:
   Click "Advanced" → "Add Environment Variable" and add:
   
   **Required (Set as Secrets)**:
   - `SPLITWISE_CLIENT_ID` - Your Splitwise OAuth Client ID (mark as Secret)
   - `SPLITWISE_CLIENT_SECRET` - Your Splitwise OAuth Client Secret (mark as Secret)
   - `SPLITWISE_REDIRECT_URI` - `https://YOUR-SERVICE-NAME.onrender.com/auth/callback`
     (Replace YOUR-SERVICE-NAME with your actual service name)
   
   **Optional** (already in render.yaml, but you can override):
   - `BASE_CURRENCY` - Default: `USD`
   - `CORS_ORIGINS` - Default: Your service URL
   - `FRONTEND_URL` - Default: Your service URL

5. **Create Web Service**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - First build may take 5-10 minutes

6. **Access Your App**:
   - Once deployed, your app will be available at: `https://YOUR-SERVICE-NAME.onrender.com`
   - Note: Free tier services spin down after 15 minutes of inactivity
   - First request after spin-down may take 30-60 seconds to wake up

## Setting Up Splitwise OAuth

1. Go to https://secure.splitwise.com/apps
2. Click "Register new app"
3. Fill in:
   - **Name**: SplitSense (or your app name)
   - **Description**: Splitwise Analytics Dashboard
   - **Callback URL**: `https://YOUR-SERVICE-NAME.onrender.com/auth/callback`
4. Copy the **Client ID** and **Client Secret**
5. Add them to Render as environment variables (marked as Secrets)

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure Dockerfile is in the root directory
- Verify all files are committed to git

### App Won't Start
- Check the runtime logs in Render dashboard
- Verify PORT environment variable is set (Render sets this automatically)
- Ensure start.py is executable

### OAuth Not Working
- Verify `SPLITWISE_REDIRECT_URI` matches exactly what you set in Splitwise app settings
- Check that client ID and secret are set as environment variables
- Review logs for OAuth errors

### Service Spins Down
- Free tier services auto-sleep after 15 min inactivity
- First request after sleep takes 30-60 seconds (cold start)
- This is normal for free tier - upgrade to paid plan to avoid spin-down

## Updating Your App

- Push to your connected branch (usually `main`)
- Render will automatically rebuild and redeploy
- Monitor the deployment in the Render dashboard

## Free Tier Limits

- 750 hours/month (enough for 24/7 operation of one service)
- Spins down after 15 minutes of inactivity
- 30-60 second cold start after spin-down
- 512MB RAM
- No SSL certificate (but HTTPS is provided)

For production use, consider upgrading to a paid plan for:
- No spin-down
- Faster cold starts
- More resources
- Better performance

