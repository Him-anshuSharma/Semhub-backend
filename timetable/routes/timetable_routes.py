import fastapi
from fastapi import File, Form, UploadFile
import timetable.controllers.timetable_controller as timetable_controller

router = fastapi.APIRouter()

@router.post("/get-time-table")
async def get_time_table(file: UploadFile = File(...), id:str = Form(...)):
    res = timetable_controller.createTimeTable(file=file,id = id)
    return res