## Student Name: Peter Saleeb
## Student ID: 215605322

"""
Public test suite for the meeting slot suggestion exercise.

Students can run these tests locally to check basic correctness of their implementation.
The hidden test suite used for grading contains additional edge cases and will not be
available to students.
"""
import pytest
from solution import suggest_slots


def test_single_event_blocks_overlapping_slots():
    """
    Functional requirement:
    Slots overlapping an event must not be suggested.
    """
    events = [{"start": "10:00", "end": "11:00"}]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "10:00" not in slots
    assert "10:30" not in slots
    assert "11:15" in slots

def test_event_outside_working_hours_is_ignored():
    """
    Constraint:
    Events completely outside working hours should not affect availability.
    """
    events = [{"start": "07:00", "end": "08:00"}]
    slots = suggest_slots(events, meeting_duration=60, day="2026-02-01")

    assert "09:00" in slots
    assert "16:00" in slots

def test_unsorted_events_are_handled():
    """
    Constraint:
    Event order should not affect correctness.
    """
    events = [
        {"start": "13:00", "end": "14:00"},
        {"start": "09:30", "end": "10:00"},
        {"start": "11:00", "end": "12:00"},
    ]
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert  slots[1] == "10:15"
    assert "09:30" not in slots

def test_lunch_break_blocks_all_slots_during_lunch():
    """
    Constraint:
    No meeting may start during the lunch break (12:00–13:00).
    """
    events = []
    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "12:00" not in slots
    assert "12:15" not in slots
    assert "12:30" not in slots
    assert "12:45" not in slots

"""TODO: Add at least 5 additional test cases to test your implementation."""

def test_invalid_meeting_duration_returns_empty():
    """
    Edge case:
    Invalid meeting duration should return empty list.
    """
    events = [{"start": "09:00", "end": "10:00"}]

    assert suggest_slots(events, meeting_duration="30", day="2026-02-01") == []
    assert suggest_slots(events, meeting_duration=25 * 60, day="2026-02-01") == []


def test_invalid_events_are_ignored():
    """
    Edge case:
    If events are malformed, assume no events.
    """
    events = [
        {"start": "10:00"},                     # missing end
        {"start": "11:00", "end": "10:00"},     # end before start
        {"start": "xx:yy", "end": "12:00"},     # invalid time
    ]

    slots = suggest_slots(events, meeting_duration=30, day="2026-02-01")

    assert "09:00" in slots
    assert "10:00" in slots


def test_day_not_today_assumes_no_events():
    """
    Rule:
    If day is not today, assume no events.
    """
    events = [{"start": "09:00", "end": "17:00"}]

    slots = suggest_slots(events, meeting_duration=60, day="2099-01-01")

    assert "09:00" in slots
    assert "16:00" in slots


def test_invalid_day_assumes_today():
    """
    Rule:
    Invalid day should default to today.
    """
    events = [{"start": "09:00", "end": "10:00"}]

    slots = suggest_slots(events, meeting_duration=30, day="NotADay")

    assert "09:00" not in slots
    assert "10:00" in slots


def test_meeting_cannot_extend_past_working_hours():
    """
    Constraint:
    Meeting must fully fit within working hours.
    """
    events = []

    slots = suggest_slots(events, meeting_duration=90, day="2026-02-01")

    assert "15:30" in slots      # ends at 17:00
    assert "16:00" not in slots  # would end at 17:30
