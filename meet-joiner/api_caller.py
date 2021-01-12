"""Module for retreiving data from the Google API."""

from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource


class Calendar:
    """Class for interacting with the Google Calendar API."""

    def __init__(self, creds):
        self.service = self._get_service(creds)

    def _get_service(self, creds: Credentials) -> Resource:
        """Construct a Resource for interacting with the API."""
        return build("calendar", "v3", credentials=creds)

    def events_in_time_range(
        self, min_time: datetime, max_time: datetime, max_results: int = 15
    ) -> dict:
        """Fetches the events in a given time range."""
        min_time = min_time.isoformat() + "Z"  # 'Z' indicates UTC time
        max_time = max_time.isoformat() + "Z"

        events = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=min,
                timeMax=max,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return events
