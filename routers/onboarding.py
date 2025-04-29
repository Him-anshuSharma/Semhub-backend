import os
from fastapi import APIRouter, UploadFile, File
from init import client
import json
from constants import onboarding_prompt as prompt, gemini_model
from models.onboarding import Response


router = APIRouter()

@router.post("/onboard")
async def makeprofile(
    audios: list[UploadFile] = None,
    images : list[UploadFile] = File(...)
):
    DIR = "tempfiles"
    os.makedirs(DIR,exist_ok=True)
    file_locations = []

    if audios is not None:
        #TODO
        print("have audio files")

    for image in images:
        image_path = os.path.join(DIR,image.filename)
        with open(image_path,"wb") as out_file:
            content = await image.read()
            out_file.write(content)
        file_locations.append(image_path)

    contents = [prompt]

    for file in file_locations:
        myfile = client.files.upload(file = file)
        contents.append(myfile)

    response = client.models.generate_content(
        model = gemini_model,
        contents=contents
    )
    print("gemini response", response.text)
    json_data= json.loads(response.text)
    gemini_response = Response.model_validate(json_data)
    print(gemini_response.goals)
    return gemini_response

