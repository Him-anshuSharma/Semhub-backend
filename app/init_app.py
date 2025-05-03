import os
from google import genai

import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    #firestore
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
        firebase_admin.initialize_app(cred)


client = None

def initialize_app():
    global client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment or .env file!")
    client = genai.Client(api_key=api_key)

def get_gemini_client():
    if client is None:
        raise RuntimeError("Gemini client not initialized. Call initialize_app() first.")
    return client

def initialize_services():
    initialize_firebase()
    initialize_app()