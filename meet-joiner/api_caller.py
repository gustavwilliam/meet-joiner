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
        self, min_date: datetime, max_date: datetime, max_results: int = 15
    ) -> dict:
        """Fetches the events in a given time range."""
        min_date = datetime.combine(min_date, datetime.min.time())
        max_date = datetime.combine(max_date, datetime.min.time())

        min_time = min_date.isoformat() + "Z"  # 'Z' indicates UTC time
        max_time = max_date.isoformat() + "Z"

        print(min_time, max_time)

        events = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=min_time,
                timeMax=max_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return events
