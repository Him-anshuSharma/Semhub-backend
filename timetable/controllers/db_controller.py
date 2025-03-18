from init import db
from fastapi import HTTPException
from timetable.models.timetable import Timetable
from firebase_admin.exceptions import FirebaseError

def save_timetable(timetable:Timetable,id:str):
    try:
        ref = db.collection(str).document('timetable')
        ref.set(timetable.get_day_schedule)
        return 
    except FirebaseError as e:
        return HTTPException(status_code=500,detail=str(e))