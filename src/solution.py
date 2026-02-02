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
    # TODO: Implement this function
        # Only allow weekdays
    from typing import List, Dict
from datetime import datetime

def suggest_slots(
    events: List[Dict[str, str]],
    meeting_duration: int,
    day: str
) -> List[str]:

    # Validate meeting duration
    if not isinstance(meeting_duration, int) or meeting_duration <= 0 or meeting_duration > 24 * 60:
        return []

    WORK_START = 9 * 60    # 09:00
    WORK_END = 17 * 60    # 17:00
    WEEKDAYS = {"Mon", "Tue", "Wed", "Thu", "Fri"}

    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m

    def to_time_str(minutes: int) -> str:
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    # Determine today's day abbreviation
    today = datetime.today().strftime("%a")

    # If invalid day provided, assume today
    if day not in WEEKDAYS:
        day = today

    # If day is not today, assume no events
    if day != today:
        events = []

    # Try to parse events; if anything is invalid, assume no events
    busy_intervals = []
    try:
        for e in events:
            start = to_minutes(e["start"])
            end = to_minutes(e["end"])
            if start >= end:
                raise ValueError
            busy_intervals.append((start, end))
    except Exception:
        busy_intervals = []

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
