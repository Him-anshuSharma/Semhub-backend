import os
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}
TEMP_DIR = "timetable/temp_files"
PROMPT = "Extract course names and their corresponding slots from the given timetable image. Provide the output in plain text from column 'slot' and 'course' and no 'venue' as slot-course"
CHAT_PROMPT = CHAT_PROMPT = '''
If the user asks for a strategy (e.g., study strategy, preparation strategy, exam strategy, etc.),
respond with 10 YouTube video links that are:
- Relevant to the topic mentioned
- Sorted by view count (highest to lowest)
- Published within the last 2 years

Respond in the following format as plain string without endline and anything extra:
{
  "topic": "<user_topic>",
  "totalVideos": 10,
  "videos": [
    {
      "title": "<video_title>",
      "url": "<video_url>",
      "views": <view_count>,
      "publishedDate": "<ISO_8601_date>"
    },
    ...
  ]
}

Otherwise, use internet and reasoning to answer the question.
'''


GOOGLE_CLIENT_ID = os.getenv("client_id")
GOOGLE_CLIENT_SECRET = os.getenv("client_secret")
GOOGLE_REDIRECT_URI = os.getenv("redirect_uris")