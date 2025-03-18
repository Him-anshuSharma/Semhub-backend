from init import db
from timetable.models.timetable import Timetable

def save_timetable(timetable:Timetable,id:str):
    ref = db.collection(str).document('timetable')
    ref.set(timetable.get_day_schedule)
    return True