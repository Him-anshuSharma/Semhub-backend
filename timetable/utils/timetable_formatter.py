import datetime
import json
from pathlib import Path
from typing import Dict, List
from timetable.models.timetable_model import Timetable, ScheduleEntry


def make_time_table(timetable) -> Timetable:
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = {key: [] for key in days}
    file_path = Path(__file__).parent / "timetable_slots.json"
    
    with open(file_path, 'r') as file:
        slots = json.load(file)
    
    for sub in timetable:
        sub_slots = sub[0].split('+')
        sub_name = sub[2]
        for slot in sub_slots:
            if slot.lower().strip() == "nil":
                continue
            for day_time in slots[slot.strip()]:
                schedule[day_time[0]].append(ScheduleEntry(time=day_time[1], subject=sub_name.strip()))
    
    return merge_and_sort_slots(schedule)

def convert_to_24hr(time_str: str) -> str:
    return datetime.datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")

def time_difference(end_time: str, start_time: str) -> float:
    end_dt = datetime.datetime.strptime(end_time, "%H:%M")
    start_dt = datetime.datetime.strptime(start_time, "%H:%M")
    return (start_dt - end_dt).total_seconds() / 60  # Convert to minutes

def merge_and_sort_slots(schedule: Dict[str, List[ScheduleEntry]]) -> Timetable:
    merged_schedule = {}

    for day, slots in schedule.items():
        formatted_slots = []

        # Convert time to 24-hour format and sort
        for slot in slots:
            start, end = slot.time.split(" - ")
            formatted_slots.append((convert_to_24hr(start), convert_to_24hr(end), slot.subject))

        formatted_slots.sort()

        merged_slots = []
        for start, end, subject in formatted_slots:
            if (merged_slots and 
                time_difference(merged_slots[-1][1], start) <= 1 and  # Allow 1-min gap
                merged_slots[-1][2] == subject):  # Same subject
                
                # Extend previous slot
                merged_slots[-1] = (merged_slots[-1][0], end, subject)
            else:
                # Add new slot
                merged_slots.append((start, end, subject))

        # Convert back to 12-hour format
        merged_schedule[day] = [
            ScheduleEntry(
                time=datetime.datetime.strptime(s, "%H:%M").strftime("%I:%M %p") + " - " +
                     datetime.datetime.strptime(e, "%H:%M").strftime("%I:%M %p"),
                subject=subj
            ) for s, e, subj in merged_slots
        ]
    
    return Timetable(days=merged_schedule)
