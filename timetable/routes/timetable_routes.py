import fastapi
from fastapi import UploadFile
import timetable.controllers.timetable_parser as timetable_controller

router = fastapi.APIRouter()

@router.post("/get-time-table")
async def get_time_table(file: UploadFile):
    return timetable_controller.createTimeTable(file=file)