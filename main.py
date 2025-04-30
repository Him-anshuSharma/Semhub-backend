from dotenv import load_dotenv

# Load .env at the very start!
load_dotenv()

from fastapi import FastAPI
from app.routers import onboarding_routes
from app.init import client
from db.init import engine
from sqlalchemy import text

app = FastAPI(title="My FastAPI Backend", version="1.0.0")
app.include_router(onboarding_routes.router, prefix="/api/v2", tags=["onboarding"])

@app.get("/")
async def read_root():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return result.scalar()