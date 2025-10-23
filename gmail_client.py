# gmail_client.py
import os, datetime, email.utils
from typing import List, Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def build_service_from_token(token_path: str):
    """Create a Gmail API service from a stored token file."""
    if not os.path.exists(token_path):
        raise FileNotFoundError(f"Token not found: {token_path}")

    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RuntimeError(f"Token invalid and cannot refresh: {token_path}")

    return build("gmail", "v1", credentials=creds)

def iso_date_from_header(date_header: str) -> str:
    try:
        dt = email.utils.parsedate_to_datetime(date_header)
        return dt.astimezone().isoformat()
    except Exception:
        return ""

def fetch_unread(service, max_results=10) -> List[Dict]:
    """Return a list of unread email summaries."""
    res = service.users().messages().list(userId="me", q="is:unread", maxResults=max_results).execute()
    messages = res.get("messages", [])
    out = []

    for m in messages:
        try:
            msg = service.users().messages().get(userId="me", id=m["id"]).execute()
            headers = {h["name"]: h["value"] for h in msg["payload"].get("headers", [])}
            out.append({
                "id": m["id"],
                "from": headers.get("From", ""),
                "subject": headers.get("Subject", ""),
                "date": iso_date_from_header(headers.get("Date", "")),
                "snippet": msg.get("snippet", "")
            })
        except Exception as e:
            print(f"Failed to fetch unread message {m['id']}: {e}")
            continue
    return out

def get_account_email(service) -> str:
    prof = service.users().getProfile(userId="me").execute()
    return prof.get("emailAddress", "")
