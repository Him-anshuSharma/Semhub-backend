import os
from google import genai

# Do NOT call load_dotenv() here; it's already called in main.py
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set in environment or .env file!")

client = genai.Client(api_key=api_key)
