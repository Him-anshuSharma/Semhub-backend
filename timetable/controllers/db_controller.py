import json
from init import db
from fastapi import HTTPException
from firebase_admin.exceptions import FirebaseError
from timetable.models.timetable_model import Timetable

def save_timetable(timetable:Timetable,id:str):
    try:
        ref = db.collection('timetable').document(id)
        timetable_dict = timetable.model_dump(mode="json")  # Ensures proper JSON serialization
    
        ref.set(timetable_dict) 
        return 
    except FirebaseError as e:
        return HTTPException(status_code=500,detail=str(e))