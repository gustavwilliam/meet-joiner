"""Module for managing and storing Events."""

import webbrowser
from datetime import date, datetime, timedelta
from typing import List

from api_caller import Calendar


class Event:
    """Extracts and stores information from API event response."""

    def __init__(self, api_response: dict) -> None:
        self.id: str = api_response["id"]
        self.title = api_response["summary"]
        self.start_time = datetime.fromisoformat(api_response["start"]["dateTime"])
        self.end_time = datetime.fromisoformat(api_response["end"]["dateTime"])

        try:
            self.meeting_link = api_response["conferenceData"]["entryPoints"][0]["uri"]
        except KeyError:
            self.meeting_link = None

    def connect_to_meeting(self) -> None:
        """Open the event meeting link in the default browser, if one exists."""
        if self.meeting_link:
            webbrowser.open(self.meeting_link)
        else:
            raise AttributeError(f"No meeting link is defined for '{self.title}'.")


def events_on_date(target: date, calendar: Calendar) -> List[Event]:
    """
    Get all events of a chosen day day.

    Returns a list of Event objects.
    """
    tomorrow = target + timedelta(days=1)

    return [
        Event(event)
        for event in calendar.events_in_time_range(min_date=target, max_date=tomorrow)[
            "items"
        ]
    ]
