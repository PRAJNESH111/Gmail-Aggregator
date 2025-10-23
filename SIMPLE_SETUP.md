# Simple Setup Guide - Direct Credentials

## Overview
This guide shows you how to set up your Gmail application using direct credentials in the code. This is the simplest approach for quick deployment.

## Step 1: Get Your Google Client Secret

### 1. Go to Google Cloud Console
- Visit [Google Cloud Console](https://console.cloud.google.com/)
- Go to "APIs & Services" > "Credentials"
- Find your OAuth client ID: `751526289871-iptd23p0suo93afht7996jm1stbt9e4f.apps.googleusercontent.com`
- Click on it to view details
- Copy the **Client Secret**

### 2. Update app.py
Replace the placeholder client secret in `app.py`:

```python
"client_secret": "YOUR_ACTUAL_CLIENT_SECRET_HERE",  # Replace with your actual client secret
```

## Step 2: Configure Redirect URIs

### 1. In Google Cloud Console
- Go to your OAuth client
- Add these authorized redirect URIs:
  - `http://localhost:5000/oauth2callback` (for local development)
  - `https://your-app-name.onrender.com/oauth2callback` (for production)

### 2. Update app.py
Replace the production URL in `app.py`:

```python
"redirect_uris": [
    "http://localhost:5000/oauth2callback",  # For local development
    "https://your-actual-app-name.onrender.com/oauth2callback"  # Update with your actual Render URL
]
```

## Step 3: Deploy to Render

### 1. Push to GitHub
```bash
git add .
git commit -m "Add direct credentials configuration"
git push origin main
```

### 2. Deploy on Render
- Go to [render.com](https://render.com)
- Connect your GitHub repository
- Render will automatically detect the `render.yaml` file
- Deploy your application

### 3. Update Redirect URI
- After deployment, get your Render app URL
- Update the redirect URI in both:
  - Google Cloud Console
  - `app.py` file (if needed)

## Step 4: Test Your Application

### Local Development
1. **Start your application:**
   ```bash
   python app.py
   ```

2. **Test OAuth flow:**
   - Go to `http://localhost:5000`
   - Click "Add User"
   - Complete the OAuth flow

### Production Testing
1. **Go to your Render app URL**
2. **Click "Add User"**
3. **Complete the OAuth flow**

## Important Notes

### Security Considerations
- **Client Secret**: Keep your client secret secure
- **Code Repository**: Consider using environment variables for production
- **Access Control**: Limit who can access your application

### Redirect URI Configuration
- **Development**: `http://localhost:5000/oauth2callback`
- **Production**: `https://your-app-name.onrender.com/oauth2callback`
- **Both must be added** in Google Cloud Console

## Troubleshooting

### Common Issues

1. **"Invalid client" error**
   - Check that your Client ID and Secret are correct
   - Verify the redirect URI matches exactly

2. **"Redirect URI mismatch" error**
   - Ensure the redirect URI in Google Console matches your app
   - Check both development and production URLs

3. **OAuth consent screen issues**
   - Configure the OAuth consent screen in Google Console
   - Add your email as a test user if needed

### Quick Fixes

1. **Update redirect URI in Google Console:**
   - Go to APIs & Services > Credentials
   - Click on your OAuth client
   - Add the correct redirect URI
   - Save changes

2. **Test locally first:**
   - Always test the OAuth flow locally before deploying
   - Use `http://localhost:5000/oauth2callback` for local testing

## Next Steps

1. **Get your Client Secret** from Google Cloud Console
2. **Update app.py** with the actual client secret
3. **Deploy to Render**
4. **Update redirect URI** in Google Console with your Render URL
5. **Test the application**

## Support

- **Google Cloud Console**: [console.cloud.google.com](https://console.cloud.google.com/)
- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Gmail API Documentation**: [developers.google.com/gmail/api](https://developers.google.com/gmail/api)
