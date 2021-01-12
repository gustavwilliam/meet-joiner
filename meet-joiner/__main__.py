"""Module with the public methods of the package."""

from datetime import date
from typing import List

from api_caller import Calendar
from auth import get_credentials
from user_interface import pick, confirm
from events import events_on_date, Event


def pick_and_connect(events: List[Event]) -> None:
    """
    Allows the user to pick an event and opens it in the browser, if a meeting link exists.

    If no meeting link is present, the user is asked if they want to try picking a different event.
    """
    event = pick(events, "Pick an event to connect to:")

    try:
        event.connect_to_meeting()
        print("Connecting...")
    except AttributeError as e:
        if confirm(f"{e} Choose another event?"):
            pick_and_connect(events)


def main() -> None:
    """Main function."""
    calendar = Calendar(get_credentials())
    events = events_on_date(date.today(), calendar)

    if events:
        pick_and_connect(events)
    else:
        print("You have no events today.")


if __name__ == "__main__":
    main()
