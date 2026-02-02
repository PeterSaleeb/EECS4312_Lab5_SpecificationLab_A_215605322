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
    if day not in {"Mon", "Tue", "Wed", "Thu", "Fri"}:
        return []

    WORK_START = 9 * 60    # 09:00
    WORK_END = 17 * 60    # 17:00

    def to_minutes(t: str) -> int:
        h, m = map(int, t.split(":"))
        return h * 60 + m

    def to_time_str(minutes: int) -> str:
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    # Convert and sort events
    busy_intervals = sorted(
        [(to_minutes(e["start"]), to_minutes(e["end"])) for e in events],
        key=lambda x: x[0]
    )

    available_starts = []

    current_time = WORK_START

    for start, end in busy_intervals:
        # Check if there is free space before this event
        while current_time + meeting_duration <= min(start, WORK_END):
            available_starts.append(to_time_str(current_time))
            current_time += 1  # granularity: 1 minute

        # Move current_time forward if overlapping
        if current_time < end:
            current_time = max(current_time, end)

    # Check remaining time after last event
    while current_time + meeting_duration <= WORK_END:
        available_starts.append(to_time_str(current_time))
        current_time += 1

    return available_starts