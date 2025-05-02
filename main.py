from dotenv import load_dotenv

# Load .env at the very start!
load_dotenv()

from fastapi import FastAPI
from app.routers import onboarding_routes
from sqlalchemy import text

import init

# Initialize application services and database
init.initialize_services()

app = FastAPI(title="My FastAPI Backend", version="1.0.0")
app.include_router(onboarding_routes.router, prefix="/api/v2", tags=["onboarding"])

@app.get("/")
async def health_check():
    engine = init.get_db_engine()
    with engine.connect() as db_connection:
        query_result = db_connection.execute(text("SELECT 1"))
        return {"status": query_result.scalar()}
