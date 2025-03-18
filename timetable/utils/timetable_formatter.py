import datetime
import json
from pathlib import Path


##helper functions
def make_time_table(timetable):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = {key:[] for key in days}
    file_path = Path(__file__).parent / "timetable_slots.json"
    with open(file_path, 'r') as file:
        slots = json.load(file)
    for sub in timetable:
        sub_slots = sub[0].split('+')
        sub_name = sub[2]
        for slot in sub_slots:
            if(slot.lower().strip() == "nil"):
                continue
            for day_time in slots[slot.strip()]:
                schedule[day_time[0]].append([day_time[1],sub_name.strip()])
    print(schedule)
    return merge_and_sort_slots(schedule)

def convert_to_24hr(time_str):
    return datetime.datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")

def time_difference(end_time, start_time):
    end_dt = datetime.datetime.strptime(end_time, "%H:%M")
    start_dt = datetime.datetime.strptime(start_time, "%H:%M")
    return (start_dt - end_dt).total_seconds() / 60  # Convert to minutes

def merge_and_sort_slots(schedule):
    merged_schedule = {}

    for day, slots in schedule.items():
        formatted_slots = []

        # Convert time to 24-hour format and sort
        for slot in slots:
            start, end = slot[0].split(" - ")
            formatted_slots.append((convert_to_24hr(start), convert_to_24hr(end), slot[1]))

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
        merged_schedule[day] = [[datetime.datetime.strptime(s, "%H:%M").strftime("%I:%M %p") + " - " +
                                 datetime.datetime.strptime(e, "%H:%M").strftime("%I:%M %p"), subj] 
                                for s, e, subj in merged_slots]

    return merged_schedule



