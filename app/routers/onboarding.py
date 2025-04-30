from fastapi import APIRouter, UploadFile, File
from app.services.onboarding import makeprofile


router = APIRouter()

@router.post("/onboard")
async def onboard(
    audios: list[UploadFile] = None,
    images : list[UploadFile] = File(...)
):
    tasks_goals = await makeprofile(audios, images)
    return tasks_goals

