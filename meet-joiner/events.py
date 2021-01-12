"""Module for managing and storing Events."""

from datetime import datetime


class Event:
    """Extracts and stores information from API event response."""

    def __init__(self, api_response: dict) -> None:
        self.id: str = api_response["id"]
        self.start_time = datetime.fromisoformat(api_response["start"]["dateTime"])
        self.end_time = datetime.fromisoformat(api_response["end"]["dateTime"])

        try:
            self.meeting_link = api_response["conferenceData"]["entryPoints"][0]["uri"]
        except KeyError:
            self.meeting_link = None
