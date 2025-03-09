from dotenv import load_dotenv
from google import genai
import os

load_dotenv('.env')
gemini = genai.Client(api_key=os.getenv('gemini_key'))