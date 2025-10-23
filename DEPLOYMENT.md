# Gmail Multi-User Dashboard - Render Deployment Guide

## Prerequisites

1. **GitHub Repository**: Push your code to a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Google Cloud Console Setup**: You'll need to configure OAuth credentials

## Step 1: Prepare Your Repository

### Files Structure
```
gmail-multi/
├── app.py
├── gmail_client.py
├── bootstrap_auth.py
├── frontend.html
├── requirements.txt
├── render.yaml
├── Procfile
├── .gitignore
├── tokens/
│   └── .gitkeep
└── credentials.json (you need to add this)
```

### Important Notes
- **credentials.json**: You need to add your Google OAuth credentials file
- **tokens/**: This directory will be created automatically on Render
- **SSL**: Render provides HTTPS automatically, so no SSL certificates needed

## Step 2: Configure Google OAuth

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
  - `https://your-app-name.onrender.com/oauth2callback`
  - `https://your-app-name.onrender.com/`
- Download the JSON file and rename it to `credentials.json`

## Step 3: Deploy to Render

### Method 1: Using render.yaml (Recommended)

1. **Push to GitHub**: Make sure all files are in your GitHub repository
2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Click "New" > "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

### Method 2: Manual Setup

1. **Create New Web Service**:
   - Go to Render Dashboard
   - Click "New" > "Web Service"
   - Connect your GitHub repository

2. **Configure Settings**:
   - **Name**: `gmail-multi-app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

3. **Environment Variables**:
   - `FLASK_ENV`: `production`
   - `FLASK_DEBUG`: `false`

## Step 4: Post-Deployment Setup

### 1. Access Your App
- Your app will be available at `https://your-app-name.onrender.com`
- The first time you access it, you'll see the dashboard

### 2. Add Users
- Click "Add User" button
- This will redirect to Google OAuth
- Complete the OAuth flow
- You'll be redirected back to your app

### 3. Test Functionality
- Select "Unread" or "Latest" mode
- Choose a user from the sidebar
- View their emails in the main area

## Important Considerations

### Security
- **credentials.json**: Contains sensitive OAuth data - keep it secure
- **tokens/**: Contains user access tokens - these are automatically managed
- **HTTPS**: Render provides SSL automatically

### Limitations
- **Free Tier**: Render free tier has limitations:
  - App sleeps after 15 minutes of inactivity
  - Cold start takes ~30 seconds
  - 750 hours/month limit

### Scaling
- **Paid Plans**: For production use, consider Render's paid plans
- **Database**: For production, consider adding a database for token storage
- **Monitoring**: Set up monitoring and logging

## Troubleshooting

### Common Issues

1. **App Not Starting**:
   - Check the logs in Render dashboard
   - Ensure all dependencies are in requirements.txt
   - Verify the start command is correct

2. **OAuth Issues**:
   - Verify redirect URIs in Google Cloud Console
   - Check that credentials.json is properly uploaded
   - Ensure HTTPS is used (not HTTP)

3. **CORS Issues**:
   - Flask-CORS is already configured
   - Check browser console for errors

4. **Token Issues**:
   - Tokens are stored in the `tokens/` directory
   - They persist between deployments
   - If issues occur, users may need to re-authenticate

### Logs
- Check Render dashboard for application logs
- Use browser developer tools for frontend debugging
- Monitor the console for any JavaScript errors

## Production Recommendations

1. **Upgrade to Paid Plan**: For better performance and reliability
2. **Add Database**: Consider PostgreSQL for token storage
3. **Add Monitoring**: Set up error tracking and performance monitoring
4. **Backup Strategy**: Implement regular backups of user tokens
5. **Security**: Review and update OAuth scopes as needed

## Support

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- **Google Gmail API**: [developers.google.com/gmail/api](https://developers.google.com/gmail/api)
