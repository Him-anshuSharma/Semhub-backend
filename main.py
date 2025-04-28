import os
from dotenv import load_dotenv

# Load .env at the very start!
load_dotenv()

from fastapi import FastAPI
from routers import onboarding
from init import client  # Now GEMINI_API_KEY is loaded before this runs

app = FastAPI(title="My FastAPI Backend", version="1.0.0")
app.include_router(onboarding.router, prefix="/api/v2", tags=["onboarding"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to your FastAPI backend!"}
