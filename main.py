from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

from db.init_db import initialize_database
initialize_database()

# Initialize other services
from app.init_app import initialize_services
initialize_services()

# Import routers AFTER initialization
from app.routers import onboarding_routes,goal_routes,task_routes,subtask_routes
app.include_router(task_routes.router,prefix="/v2/task")
app.include_router(onboarding_routes.router,prefix="/v2/onboarding")
app.include_router(goal_routes.router,prefix="/v2/goal")
app.include_router(subtask_routes.router,prefix="/v2/subtask")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
