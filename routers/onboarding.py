from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter()

@router.post("/onboard")
async def makeprofile(
    images: List[UploadFile] = File(..., description="List of image files"),
    audios: List[UploadFile] = File(..., description="List of audio files")
):
    