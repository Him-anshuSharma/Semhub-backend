
from datetime import datetime
from fastapi import FastAPI, HTTPException,UploadFile
from google import genai
from PIL import Image
import os
import shutil
import json
from dotenv import load_dotenv

app = FastAPI()
load_dotenv('.env')


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}
TEMP_DIR = "temp_files"

prompt = "Extract course names and their corresponding slots from the given timetable image. Provide the output in plain text from column 'slot' and 'course' and no 'venue' as slot-course"

gemini = genai.Client(api_key=os.getenv('gemini_key'))

# Define allowed extensions
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}


@app.get("/")
def read_root():
    return {"Hello ": "World"}

@app.get("/test")
def test_api():
    response = gemini.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hey Gemini!",
    )
    return {"response":response.text}

@app.post("/get-time-table")
async def get_time_table(file: UploadFile):

    # Validate file type
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Allowed: PNG, JPG, JPEG, PDF")

    # Ensure temp directory exists
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Load the image
        image = Image.open(file_path)

        # Generate response using Gemini AI
        response = gemini.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt, image]
        )

        # Process response
        response_lines = response.text.strip().split("\n")
        processed_response = [line.split("-") for line in response_lines]

        #print(processed_response)

        return make_time_table(processed_response)


    finally:
        # Cleanup: Remove file after processing
        os.remove(file_path)

def make_time_table(timetable):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = {key:[] for key in days}
    with open('slots.json', 'r') as file:
        slots = json.load(file)
    for sub in timetable:
        sub_slots = sub[0].split('+')
        sub_name = sub[2]
        for slot in sub_slots:
            if(slot.lower().strip() == "nil"):
                continue
            for day_time in slots[slot.strip()]:
                schedule[day_time[0]].append([day_time[1],sub_name.strip()])
    return merge_and_sort_slots(schedule)

def convert_to_24hr(time_str):
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")

def time_difference(end_time, start_time):
    end_dt = datetime.strptime(end_time, "%H:%M")
    start_dt = datetime.strptime(start_time, "%H:%M")
    return (start_dt - end_dt).total_seconds() / 60  # Convert to minutes

def merge_and_sort_slots(schedule):
    merged_schedule = {}

    for day, slots in schedule.items():
        formatted_slots = []

        # Convert time to 24-hour format and sort
        for slot in slots:
            start, end = slot[0].split(" - ")
            formatted_slots.append((convert_to_24hr(start), convert_to_24hr(end), slot[1]))

        formatted_slots.sort()

        merged_slots = []
        for start, end, subject in formatted_slots:
            if (merged_slots and 
                time_difference(merged_slots[-1][1], start) <= 1 and  # Allow 1-min gap
                merged_slots[-1][2] == subject):  # Same subject
                
                # Extend previous slot
                merged_slots[-1] = (merged_slots[-1][0], end, subject)
            else:
                # Add new slot
                merged_slots.append((start, end, subject))

        # Convert back to 12-hour format
        merged_schedule[day] = [[datetime.strptime(s, "%H:%M").strftime("%I:%M %p") + " - " +
                                 datetime.strptime(e, "%H:%M").strftime("%I:%M %p"), subj] 
                                for s, e, subj in merged_slots]

    return merged_schedule

# Example input
schedule = {  
    "Monday": [
        ["05:40 PM - 06:30 PM", "Penetration Testing and Vulnerability Analysis Lab (Lab Only)"],
        ["06:31 PM - 07:20 PM", "Penetration Testing and Vulnerability Analysis Lab (Lab Only)"]
    ],
    "Tuesday": [
        ["05:40 PM - 06:30 PM", "Malware Analysis Lab (Lab Only)"],
        ["06:31 PM - 07:20 PM", "Malware Analysis Lab (Lab Only)"]
    ]
}

