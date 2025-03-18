from fastapi import APIRouter, HTTPException
from timetable.models.timetable import Timetable
from timetable.controllers.db_controller import save_timetable

router = APIRouter();

@router.post("/save-user-timetable")
async def save_user_timetable(timetable:Timetable,id:str):
    try:
        save_timetable(timetable,id)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))