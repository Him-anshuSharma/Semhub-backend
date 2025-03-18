import json
from pydantic import BaseModel

class Timetable(BaseModel):
    def __init__(self, schedule):
        self.schedule = schedule  # Directly store the passed schedule

    def get_day_schedule(self, day):
        """Get the schedule for a specific day."""
        return self.schedule.get(day, [])

    def get_full_schedule(self):
        """Get the complete schedule."""
        return self.schedule

    def __repr__(self):
        return json.dumps(self.schedule, indent=2)
