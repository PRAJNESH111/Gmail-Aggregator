# .env File Setup Guide

## Quick Setup Steps

### 1. Copy the example file
```bash
cp env.example .env
```

### 2. Edit your .env file
Open `.env` and replace `your_client_secret_here` with your actual Google Client Secret:

```env
# Google OAuth Credentials
GOOGLE_CLIENT_ID=751526289871-iptd23p0suo93afht7996jm1stbt9e4f.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=YOUR_ACTUAL_CLIENT_SECRET_HERE
GOOGLE_REDIRECT_URI=http://localhost:5000/oauth2callback

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=true
PORT=5000
```

### 3. Get your Client Secret
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "Credentials"
3. Find your OAuth client ID: `751526289871-iptd23p0suo93afht7996jm1stbt9e4f.apps.googleusercontent.com`
4. Click on it and copy the **Client Secret**
5. Replace `YOUR_ACTUAL_CLIENT_SECRET_HERE` in your `.env` file

### 4. Configure Redirect URIs in Google Console
Add these redirect URIs in Google Cloud Console:
- `http://localhost:5000/oauth2callback` (for local development)
- `https://your-app-name.onrender.com/oauth2callback` (for production)

### 5. Test locally
```bash
python app.py
```

## For Production (Render)

### Option 1: Use Environment Variables in Render
1. Go to your Render dashboard
2. Go to your service > Environment
3. Add these environment variables:
   - `GOOGLE_CLIENT_ID`: `751526289871-iptd23p0suo93afht7996jm1stbt9e4f.apps.googleusercontent.com`
   - `GOOGLE_CLIENT_SECRET`: Your actual client secret
   - `GOOGLE_REDIRECT_URI`: `https://your-app-name.onrender.com/oauth2callback`

### Option 2: Update .env for production
Create a production .env file with your Render URL:
```env
GOOGLE_CLIENT_ID=751526289871-iptd23p0suo93afht7996jm1stbt9e4f.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_actual_client_secret_here
GOOGLE_REDIRECT_URI=https://your-app-name.onrender.com/oauth2callback
FLASK_ENV=production
FLASK_DEBUG=false
```

## Security Notes

- **Never commit .env files** to git (they're already in .gitignore)
- **Keep your client secret secure**
- **Use different credentials for development and production**

## Troubleshooting

### "No OAuth credentials found" error
- Make sure your `.env` file exists and has the correct values
- Check that the variable names match exactly
- Verify you have the `python-dotenv` package installed

### OAuth redirect mismatch
- Ensure the redirect URI in Google Console matches your `.env` file
- For local: `http://localhost:5000/oauth2callback`
- For production: `https://your-app-name.onrender.com/oauth2callback`

## File Structure
```
gmail-multi/
├── .env                    # Your local environment variables (not in git)
├── env.example             # Template file (safe to commit)
├── app.py                  # Updated to load .env file
├── requirements.txt        # Includes python-dotenv
└── ...
```

## Next Steps
1. Copy `env.example` to `.env`
2. Get your client secret from Google Cloud Console
3. Update `.env` with your actual client secret
4. Test locally with `python app.py`
5. Deploy to Render
