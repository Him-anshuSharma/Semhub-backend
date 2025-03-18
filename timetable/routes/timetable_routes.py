import fastapi
from fastapi import UploadFile
import timetable.controllers.timetable_controller as timetable_controller

router = fastapi.APIRouter()

@router.post("/get-time-table")
async def get_time_table(file: UploadFile):
    res = timetable_controller.createTimeTable(file=file)
    return res