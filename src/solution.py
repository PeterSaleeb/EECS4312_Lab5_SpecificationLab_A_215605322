## Student Name: Peter Saleeb
## Student ID: 215605322

"""
Stub file for the meeting slot suggestion exercise.

Implement the function `suggest_slots` to return a list of valid meeting start times
on a given day, taking into account working hours, and possible specific constraints. See the lab handout
for full requirements.
"""
from typing import List, Dict

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:
    """
    Suggest possible meeting start times for a given day.

    Args:
        events: List of dicts with keys {"start": "HH:MM", "end": "HH:MM"}
        meeting_duration: Desired meeting length in minutes
        day: Three-letter day abbreviation (e.g., "Mon", "Tue", ... "Fri")

    Returns:
        List of valid start times as "HH:MM" sorted ascending
    """

from typing import List, Dict
from datetime import datetime, timedelta

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:

    # Validate meeting duration
    if not isinstance(meeting_duration, int) or meeting_duration <= 0 or meeting_duration > 24 * 60:
        return []

    WORK_START = 9 * 60
    WORK_END = 17 * 60
    LUNCH_START = 12 * 60
    LUNCH_END = 13 * 60

    WEEKDAY_INDEX = {
        "mon": 0, "tue": 1, "wed": 2,
        "thu": 3, "fri": 4, "sat": 5, "sun": 6
    }

    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m

    def to_time_str(minutes: int) -> str:
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    # Resolve requested day to a concrete date
    today = datetime.today().date()
    day_lower = day.lower()

    try:
        # Case 1: explicit date YYYY-MM-DD
        target_date = datetime.strptime(day, "%Y-%m-%d").date()
    except ValueError:
        # Case 2: weekday abbreviation
        if day_lower in WEEKDAY_INDEX:
            target_weekday = WEEKDAY_INDEX[day_lower]
            delta = (target_weekday - today.weekday()) % 7
            if delta == 0:
                delta = 7  # next occurrence, not today
            target_date = today + timedelta(days=delta)
        else:
            target_date = datetime.today().date() 

    target_date_str = target_date.strftime("%Y-%m-%d")

    # Parse events
    busy_intervals = [(LUNCH_START, LUNCH_END)]

    if target_date.weekday() == 4: # no events after 3pm on friday
        busy_intervals.append((15*60, 17*60))

    for e in events:
        try:
            if e.get("day") != target_date_str:
                continue

            start = to_minutes(e["start"])
            end = to_minutes(e["end"])

            if start >= end:
                continue

            busy_intervals.append((start, end))
        except Exception:
            continue  # ignore malformed event only

    busy_intervals.sort(key=lambda x: x[0])

    available_starts = []
    current_time = WORK_START

    for start, end in busy_intervals:
        while current_time + meeting_duration <= min(start, WORK_END):
            available_starts.append(to_time_str(current_time))
            current_time += 1

        if current_time < end:
            current_time = max(current_time, end)

    while current_time + meeting_duration <= WORK_END:
        available_starts.append(to_time_str(current_time))
        current_time += 1

    return available_starts
