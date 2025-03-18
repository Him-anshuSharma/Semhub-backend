from dotenv import load_dotenv
from google import genai
import os
import firebase_admin
from firebase_admin import credentials,firestore

load_dotenv('.env')

#firestore
cred = credentials.Certificate(os.getenv('db_creds_path'))
firebase_admin.initialize_app(cred)
db = firestore.client()

#gemini
gemini = genai.Client(api_key=os.getenv('gemini_key'))
