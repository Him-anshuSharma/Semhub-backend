import os
from google import genai

_gemini_client = None

def initialize_app():
    global _gemini_client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment or .env file!")
    _gemini_client = genai.Client(api_key=api_key)

def get_gemini_client():
    if _gemini_client is None:
        raise RuntimeError("Gemini client not initialized. Call initialize_app() first.")
    return _gemini_client
