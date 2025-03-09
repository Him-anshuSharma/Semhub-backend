import os
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}
TEMP_DIR = "timetable/temp_files"
PROMPT = "Extract course names and their corresponding slots from the given timetable image. Provide the output in plain text from column 'slot' and 'course' and no 'venue' as slot-course"
GOOGLE_CLIENT_ID = os.getenv("client_id")
GOOGLE_CLIENT_SECRET = os.getenv("client_secret")
GOOGLE_REDIRECT_URI = os.getenv("redirect_uris")