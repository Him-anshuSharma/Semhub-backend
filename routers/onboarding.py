import os
from fastapi import APIRouter, UploadFile, File
from init import client
from constants import onboarding_prompt as prompt, gemini_model


router = APIRouter()

@router.post("/onboard")
async def makeprofile(
    audio: list[UploadFile] = None,
    images : list[UploadFile] = File(...)
):
    DIR = "tempfiles"
    os.makedirs(DIR,exist_ok=True)
    file_locations = []
    for image in images:
        image_path = os.path.join(DIR,image.filename)
        with open(image_path,"wb") as out_file:
            content = await image.read()
            out_file.write(content)
        file_locations.append(image_path)
    print(image_path)
    response = client.models.generate_content(
        model = gemini_model,
        contents = ["Hi there!"]
    )

    return response.text

