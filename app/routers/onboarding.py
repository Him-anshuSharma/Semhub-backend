import os
from fastapi import APIRouter, UploadFile, File
from services.onboarding import makeprofile
from models.onboarding import Response


router = APIRouter()

@router.post("/onboard")
async def makeprofile(
    audios: list[UploadFile] = None,
    images : list[UploadFile] = File(...)
):
    tasks_goals = makeprofile(audios, images)
    return tasks_goals

