# How to Get Your Splitwise API Token

## Step-by-Step Guide

### Step 1: Log in to Splitwise
1. Go to https://www.splitwise.com
2. Log in with your Splitwise account credentials

### Step 2: Navigate to Developer Settings
1. Once logged in, go directly to: **https://secure.splitwise.com/apps**
   
   OR navigate manually:
   - Click on your profile/account settings (usually top right)
   - Look for "Developer" or "Apps" section
   - Click on it

### Step 3: Create a New App
1. On the Apps page, you'll see a list of your existing apps (if any)
2. Click the **"Create new app"** or **"Register new application"** button
3. You'll be taken to a form to register your application

### Step 4: Fill Out the Application Form
Fill in the following details:

- **Application Name**: 
  - Example: "SplitSense" or "My Expense Analyzer" or "Personal Finance Tool"
  - This is just a label for your reference

- **Description**: 
  - Example: "Personal expense analysis and insights tool"
  - Brief description of what you're using it for

- **Homepage URL**: 
  - Can be: `http://localhost:8000` or `https://github.com/GauthamPrabhuM/SplitSense`
  - Or any URL (not strictly required for personal use)

- **Redirect URI**: 
  - Can be: `http://localhost:8000` or leave blank
  - For OAuth redirects (not needed for personal access tokens)

- **Application Type**: 
  - Select **"Personal Access Token"** or **"Web Application"**
  - For this tool, either works, but Personal Access Token is simpler

### Step 5: Get Your Token
1. After submitting the form, you'll be taken to your app's details page
2. Look for a section labeled:
   - **"Personal Access Token"**
   - **"Access Token"**
   - **"API Key"**
   - **"Token"**

3. **Copy the token immediately!** 
   - ⚠️ **Important**: You may only see this token once
   - It will look like a long string of random characters
   - Example format: `abc123xyz789...` (much longer)

### Step 6: Save Your Token Securely
- **DO NOT** share this token publicly
- **DO NOT** commit it to GitHub
- Store it securely (password manager, secure notes, etc.)

## Using Your Token

### Option 1: In the Web Dashboard
1. Start the server: `./start_server.sh` or `uvicorn main:app --reload`
2. Open http://localhost:8000
3. Paste your token in the "Splitwise API Token" field
4. Click "Ingest Data"

### Option 2: As Environment Variable
```bash
export SPLITWISE_API_TOKEN=your_token_here
```

Then run:
```bash
python example_usage.py
```

### Option 3: Via API
```bash
curl -X POST "http://localhost:8000/api/ingest" \
  -H "Content-Type: application/json" \
  -d '{"api_token": "your_token_here", "base_currency": "USD"}'
```

## Troubleshooting

### Can't Find the Apps Page?
- Direct URL: https://secure.splitwise.com/apps
- Make sure you're logged in
- Try a different browser if it doesn't load

### Token Not Working?
- Verify you copied the entire token (they're usually very long)
- Check for extra spaces before/after the token
- Make sure the token hasn't expired (they usually don't expire, but check)
- Try creating a new app/token

### "Invalid Token" Error?
- Double-check the token is correct
- Make sure you're using the "Personal Access Token" not the "Consumer Key"
- Try regenerating the token

### Can't See Token After Creation?
- Some tokens are only shown once during creation
- You may need to create a new app to get a new token
- Check if there's a "Regenerate Token" or "Show Token" button

## Security Best Practices

1. **Never commit tokens to Git**
   - The `.gitignore` file already excludes `.env` files
   - Use environment variables instead

2. **Use environment variables**
   ```bash
   export SPLITWISE_API_TOKEN=your_token
   ```

3. **Create a `.env` file** (if you want to persist it locally)
   ```bash
   echo "SPLITWISE_API_TOKEN=your_token_here" > .env
   ```
   Then load it: `source .env` (make sure `.env` is in `.gitignore`)

4. **Rotate tokens periodically**
   - Delete old apps/tokens you're not using
   - Create new ones if you suspect a token was compromised

## Quick Reference

- **Apps Page**: https://secure.splitwise.com/apps
- **Splitwise Home**: https://www.splitwise.com
- **Token Format**: Long alphanumeric string (50+ characters typically)

## Need Help?

If you're still having trouble:
1. Check Splitwise's official documentation: https://dev.splitwise.com/
2. Make sure your Splitwise account is active
3. Try creating the app in an incognito/private browser window
4. Contact Splitwise support if the apps page isn't accessible

