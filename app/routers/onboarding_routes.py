from fastapi import APIRouter, UploadFile, File
from app.services.onboarding_services import makeprofile
from constants import temp_token

router = APIRouter()

@router.post("/onboard")
async def onboard(
    token: str = temp_token,
    audios: list[UploadFile] = None,
    images: list[UploadFile] = File(...),
):
    tasks_goals = await makeprofile(token, audios, images)
    return tasks_goals

