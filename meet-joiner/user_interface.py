"""Contains all utilities for the user interface."""

from typing import List
from datetime import datetime

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


def pick(events: List[Event], title: str) -> int:
    """
    Let's the user pick one of the provided options.

    Returns the chosen item.
    """
    menu_items = [_get_menu_item(event, i) for i, event in enumerate(events)]

    menu = TerminalMenu(
        menu_items,
        title=title,
    )

    chosen_item_index = menu.show()
    return events[chosen_item_index]
