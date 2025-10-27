import glob, os, json
from flask import Flask, jsonify, request, send_file, redirect
from flask_cors import CORS
from gmail_client import build_service_from_token, fetch_unread, get_account_email
from concurrent.futures import ThreadPoolExecutor
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from gmail_client import SCOPES
from pathlib import Path
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Create token directory ---
TOKENS_DIR = Path("tokens")
TOKENS_DIR.mkdir(exist_ok=True)

# --- Get OAuth credentials (from env or file) ---
def get_oauth_credentials():
    client_id = os.environ.get('GOOGLE_CLIENT_ID')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
    
    if client_id and client_secret and redirect_uri:
        credentials = {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri]
            }
        }
        return credentials
    elif os.path.exists("credentials.json"):
        with open("credentials.json", "r") as f:
            return json.load(f)
    else:
        raise FileNotFoundError("No OAuth credentials found. Please set environment variables or add credentials.json file.")

# --- Flask setup ---
app = Flask(__name__)
CORS(app)

# --- Fetch unread mails ---
def fetch_account_unread(token_path: str, max_per: int):
    try:
        service = build_service_from_token(token_path)
        email_addr = get_account_email(service)
        mails = fetch_unread(service, max_results=max_per)
        return {"email": email_addr, "count": len(mails), "messages": mails}
    except Exception as e:
        return {"email": os.path.basename(token_path), "error": str(e), "messages": []}

# --- Fetch latest mails ---
def fetch_account_latest(token_path: str, max_per: int):
    try:
        service = build_service_from_token(token_path)
        email_addr = get_account_email(service)

        results = service.users().messages().list(
            userId="me",
            labelIds=["INBOX"],
            maxResults=max_per
        ).execute()

        messages = []
        for msg in results.get("messages", []):
            try:
                msg_detail = service.users().messages().get(userId="me", id=msg["id"]).execute()
                headers = msg_detail.get("payload", {}).get("headers", [])
                msg_data = {
                    "from": next((h["value"] for h in headers if h["name"] == "From"), ""),
                    "subject": next((h["value"] for h in headers if h["name"] == "Subject"), ""),
                    "date": next((h["value"] for h in headers if h["name"] == "Date"), ""),
                    "snippet": msg_detail.get("snippet", "")
                }
                messages.append(msg_data)
            except Exception:
                continue

        return {"email": email_addr, "count": len(messages), "messages": messages}
    except Exception as e:
        return {"email": os.path.basename(token_path), "error": str(e), "messages": []}

# --- Frontend route ---
@app.route("/")
def index():
    return send_file("frontend.html")

# --- Add Gmail account (OAuth step 1) ---
@app.route("/add_user")
def add_user():
    try:
        credentials = get_oauth_credentials()
        flow = InstalledAppFlow.from_client_config(credentials, SCOPES)
        flow.redirect_uri = request.url_root + "oauth2callback"
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent"
        )
        return redirect(authorization_url)
    except Exception as e:
        return f"<p>Error setting up OAuth: {e}</p><p><a href='/'>Go to homepage</a></p>"

# --- OAuth callback ---
@app.route("/oauth2callback")
def oauth2callback():
    try:
        credentials = get_oauth_credentials()
        flow = InstalledAppFlow.from_client_config(credentials, SCOPES)
        flow.redirect_uri = request.url_root + "oauth2callback"
        flow.fetch_token(authorization_response=request.url)

        creds = flow.credentials
        service = build("gmail", "v1", credentials=creds)
        email_addr = service.users().getProfile(userId="me").execute()["emailAddress"]

        token_path = TOKENS_DIR / f"{email_addr}.json"
        with open(token_path, "w") as f:
            f.write(creds.to_json())

        has_refresh_token = hasattr(creds, 'refresh_token') and creds.refresh_token is not None
        debug_info = f"<br>Refresh token present: {has_refresh_token}"

        return f"<p>✅ Successfully added account: {email_addr}</p>{debug_info}<p><a href='/'>Go to homepage</a></p>"
    except Exception as e:
        return f"<p>Error adding account: {e}</p><p><a href='/'>Go to homepage</a></p>"

# --- Delete user route ---
@app.route("/delete_user", methods=["POST"])
def delete_user():
    try:
        data = request.get_json()
        email = data.get("email")
        if not email:
            return jsonify({"error": "Email is required"}), 400

        token_path = TOKENS_DIR / f"{email}.json"
        if not token_path.exists():
            return jsonify({"error": "User not found"}), 404

        token_path.unlink()
        return jsonify({"message": f"User {email} deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Unread mails route ---
@app.route("/unread")
def unread():
    max_per = int(request.args.get("max", 7))
    token_paths = glob.glob("tokens/*.json")
    if not token_paths:
        return jsonify({"accounts": [], "message": "No authenticated accounts found."})

    data = {"accounts": []}
    with ThreadPoolExecutor(max_workers=len(token_paths)) as executor:
        for tp in token_paths:
            data["accounts"].append(fetch_account_unread(tp, max_per))
    return jsonify(data)

# --- Latest mails route ---
@app.route("/latest")
def latest():
    max_per = int(request.args.get("max", 7))
    token_paths = glob.glob("tokens/*.json")
    if not token_paths:
        return jsonify({"accounts": [], "message": "No authenticated accounts found."})

    data = {"accounts": []}
    with ThreadPoolExecutor(max_workers=len(token_paths)) as executor:
        for tp in token_paths:
            data["accounts"].append(fetch_account_latest(tp, max_per))
    return jsonify(data)

# --- Flask entry point ---
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # Always bind to 0.0.0.0 for Render
    app.run(host='0.0.0.0', port=port, debug=False)
