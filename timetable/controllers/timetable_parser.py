from fastapi import UploadFile, HTTPException
from timetable.utils.timetable_formatter import make_time_table
import os
import constants
import shutil
from PIL import Image
from init import gemini

def createTimeTable(file:UploadFile):
     # Validate file type
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in constants.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: PNG, JPG, JPEG, PDF")

    # Ensure temp directory exists
    os.makedirs(constants.TEMP_DIR, exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(constants.TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Load the image
        image = Image.open(file_path)

        # Generate response using Gemini AI
        response = gemini.models.generate_content(
            model="gemini-2.0-flash",
            contents=[constants.PROMPT, image]
        )

        # Process response
        response_lines = response.text.strip().split("\n")
        processed_response = [line.split("-") for line in response_lines]

        #print(processed_response)

        return make_time_table(processed_response)


    finally:
        # Cleanup: Remove file after processing
        os.remove(file_path)