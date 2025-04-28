import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()


app = FastAPI(title="My FastAPI Backend", version="1.0.0")

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to your FastAPI backend!"}
