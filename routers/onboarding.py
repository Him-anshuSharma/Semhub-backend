from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
from init import client
from constants import onboarding_prompt as prompt, gemini_model
import tempfile

router = APIRouter()

@router.post("/onboard")
async def makeprofile(
):
    response = client.models.generate_content(
        model = gemini_model,
        contents = ["Hi there!"]
    )
    return response.text

