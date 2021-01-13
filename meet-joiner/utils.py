"""Contains all utilities used in the package."""

from datetime import datetime
from typing import List, Optional

import pytz
from simple_term_menu import TerminalMenu

from events import Event


def _humanize_time(time: datetime) -> str:
    """Converts a datetime object into a XX:YY format"""
    return time.strftime("%H:%M")


def _get_menu_item(event: Event, index: str) -> List[str]:
    start_time = _humanize_time(event.start_time)
    end_time = _humanize_time(event.end_time)
    title = event.title

    return f"[{index}] {start_time}–{end_time} {title}"


def pick(events: List[Event], title: str) -> Event:
    """
    Let's the user pick one of the provided options.

    Returns the chosen item.
    """
    if not events:
        raise ValueError("No events specified.")

    menu_items = [_get_menu_item(event, i) for i, event in enumerate(events)]
    closest_event = closest_event_start(events)

    menu = TerminalMenu(
        menu_items, title=title, cursor_index=events.index(closest_event)
    )

    chosen_item_index = menu.show()
    return events[chosen_item_index]


def confirm(prompt: str) -> bool:
    """
    Confirms a prompt with the user, through a yes or no question.

    Returns a boolean matching their response.
    """
    menu = TerminalMenu(
        [
            "[0] Yes",
            "[1] No",
        ],
        title=prompt,
    )

    answer = menu.show()
    return not bool(answer)  # 'not' since 'True' has the index 0 and 'False' has 1


def closest_event_start(
    events: List[Event],
    reference_time: datetime = datetime.utcnow().replace(tzinfo=pytz.UTC),
):
    """
    Gets the event with a start closest to the reference time.

    Only non-completed events will be considered. Requires a timezone aware datetime\
    object as reference. Returns None if no un-completed event was found.
    """
    events_before = [event for event in events if event.end_time > reference_time]

    closest_event: Optional[Event] = None
    if events_before:
        event = min(
            events_before, key=lambda event: abs(event.start_time - reference_time)
        )

    return closest_event
