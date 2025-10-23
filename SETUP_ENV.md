# Environment Variables Setup Guide

## Overview
This guide shows you how to set up your Gmail application using environment variables instead of a `credentials.json` file. This is more secure for production deployment.

## Step 1: Get Google OAuth Credentials

### 1. Go to Google Cloud Console
- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or select existing one

### 2. Enable Gmail API
- Go to "APIs & Services" > "Library"
- Search for "Gmail API" and enable it

### 3. Create OAuth Credentials
- Go to "APIs & Services" > "Credentials"
- Click "Create Credentials" > "OAuth client ID"
- Choose "Web application"
- Add authorized redirect URIs:
  - For development: `http://localhost:5000/oauth2callback`
  - For production: `https://your-app-name.onrender.com/oauth2callback`
- Click "Create"
- Copy the **Client ID** and **Client Secret**

## Step 2: Set Up Environment Variables

### For Local Development

1. **Copy the example file:**
   ```bash
   cp env.example .env
   ```

2. **Edit the .env file with your actual values:**
   ```env
   # Google OAuth Credentials
   GOOGLE_CLIENT_ID=your_actual_client_id_here
   GOOGLE_CLIENT_SECRET=your_actual_client_secret_here
   GOOGLE_REDIRECT_URI=http://localhost:5000/oauth2callback
   
   # Flask Configuration
   FLASK_ENV=development
   FLASK_DEBUG=true
   PORT=5000
   ```

3. **Install python-dotenv (optional but recommended):**
   ```bash
   pip install python-dotenv
   ```

4. **Update app.py to load .env file (optional):**
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # Add this at the top of app.py
   ```

### For Production (Render)

1. **In your Render dashboard:**
   - Go to your service
   - Click "Environment"
   - Add these environment variables:
     - `GOOGLE_CLIENT_ID`: 751526289871-iptd23p0suo93afht7996jm1stbt9e4f.apps.googleusercontent.com
     - `GOOGLE_CLIENT_SECRET`: Your Google Client Secret
     - `GOOGLE_REDIRECT_URI`: `https://your-app-name.onrender.com/oauth2callback`
     - `FLASK_ENV`: `production`
     - `FLASK_DEBUG`: `false`

2. **Update render.yaml with your actual values:**
   ```yaml
   envVars:
     - key: GOOGLE_CLIENT_ID
       value: your_actual_client_id_here
     - key: GOOGLE_CLIENT_SECRET
       value: your_actual_client_secret_here
     - key: GOOGLE_REDIRECT_URI
       value: https://your-app-name.onrender.com/oauth2callback
   ```

## Step 3: Test Your Setup

### Local Development
1. **Start your application:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   - Go to `http://localhost:5000`
   - Click "Add User"
   - Complete the OAuth flow

### Production (Render)
1. **Deploy your application**
2. **Test the OAuth flow:**
   - Go to your Render app URL
   - Click "Add User"
   - Complete the OAuth flow

## Security Notes

### Environment Variables vs credentials.json
- **Environment Variables**: More secure, no files to manage
- **credentials.json**: Easier for development, but less secure

### Best Practices
1. **Never commit .env files** to version control
2. **Use different credentials** for development and production
3. **Rotate credentials** regularly
4. **Use environment variables** in production

## Troubleshooting

### Common Issues

1. **"No OAuth credentials found"**
   - Check that environment variables are set correctly
   - Verify the variable names match exactly
   - Make sure you're not missing any required variables

2. **OAuth redirect mismatch**
   - Check that the redirect URI in Google Console matches your environment
   - For development: `http://localhost:5000/oauth2callback`
   - For production: `https://your-app-name.onrender.com/oauth2callback`

3. **"Invalid client" error**
   - Verify your Client ID and Client Secret are correct
   - Check that the OAuth consent screen is configured
   - Ensure the Gmail API is enabled

### Debug Steps

1. **Check environment variables:**
   ```python
   import os
   print("Client ID:", os.environ.get('GOOGLE_CLIENT_ID'))
   print("Client Secret:", os.environ.get('GOOGLE_CLIENT_SECRET'))
   print("Redirect URI:", os.environ.get('GOOGLE_REDIRECT_URI'))
   ```

2. **Test OAuth flow:**
   - Check the browser console for errors
   - Verify the redirect URL is correct
   - Check that the OAuth consent screen is properly configured

## Alternative: Using credentials.json

If you prefer to use the `credentials.json` file approach:

1. **Download credentials.json** from Google Cloud Console
2. **Place it in your project root**
3. **The app will automatically fall back** to using the file if environment variables are not set

## Migration from credentials.json to Environment Variables

If you're migrating from `credentials.json` to environment variables:

1. **Extract the values** from your `credentials.json` file:
   ```json
   {
     "web": {
       "client_id": "your_client_id",
       "client_secret": "your_client_secret",
       "redirect_uris": ["your_redirect_uri"]
     }
   }
   ```

2. **Set the environment variables** with these values
3. **Remove or ignore** the `credentials.json` file
4. **Test the application** to ensure it works

## Support

- **Google OAuth Documentation**: [developers.google.com/identity/protocols/oauth2](https://developers.google.com/identity/protocols/oauth2)
- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
