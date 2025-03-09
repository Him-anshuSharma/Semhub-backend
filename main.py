from fastapi import FastAPI
from init import gemini
from timetable.routes.timetable_routes import router as timetable_router

app = FastAPI()

app.include_router(timetable_router,prefix="/api/timetable")


@app.get("/")
def read_root():
    return {"Hello ": "World"}

@app.get("/test")
def test_api():
    response = gemini.models.generate_content(
        model="gemini-2.0-flash",
        contents="Hey Gemini!",
    )
    return {"response":response.text}