"""Functions for authenticating via the Google API."""

import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def authenticate(creds: Credentials) -> Credentials:
    """Authenticates the user and returns their credentials."""
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("meet-joiner/auth.py", SCOPES)
        creds = flow.run_local_server(port=0)

    with open("meet-joiner/token.pickle", "wb") as token:
        pickle.dump(creds, token)

    return creds


def get_credentials() -> Credentials:
    """
    Get user's access and refresh tokens.

    If none are saved locally, prompt the user to authenticate.
    """
    creds = None

    if os.path.exists("meet-joiner/token.pickle"):
        with open("meet-joiner/token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        creds = authenticate(creds)

    return creds
