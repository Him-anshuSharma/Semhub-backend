from pydantic import BaseModel
from typing import List, Dict

class ScheduleEntry(BaseModel):
    time: str
    subject: str

class Timetable(BaseModel):

    days: Dict[str, List[ScheduleEntry]]

    def getDaySchedule(self, day: str) -> List[ScheduleEntry]:
        return self.days.get(day, [])