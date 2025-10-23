# bootstrap_auth.py
import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from gmail_client import SCOPES

TOKENS_DIR = Path("tokens")
TOKENS_DIR.mkdir(exist_ok=True)

def add_account():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
    service = build("gmail", "v1", credentials=creds)
    email_addr = service.users().getProfile(userId="me").execute()["emailAddress"]

    token_path = TOKENS_DIR / f"{email_addr}.json"
    with open(token_path, "w") as f:
        f.write(creds.to_json())
    print(f"✅ Saved token for {email_addr} at: {token_path}")

if __name__ == "__main__":
    while True:
        add_account()
        more = input("Add another Gmail? (y/n): ").strip().lower()
        if more != "y":
            break
