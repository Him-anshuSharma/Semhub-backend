from fastapi import APIRouter, HTTPException

from database.controllers.db_controller import save_timetable

router = APIRouter();

@router.post("/save-user-timetable")
async def save_user_timetable(timetable:str,id:str):
    try:
        save_timetable(timetable,id)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))