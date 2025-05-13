from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.services.onboarding_services import makeprofile
from app.services.verify_firebase_token import verify_firebase_token
from db.init_db import get_session as get_db  # Replace with your actual get_db function

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])

@router.post("/onboard")
async def onboard(
    decoded_token = Depends(verify_firebase_token),
    audios: list[UploadFile] = None,
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    """
    Process user onboarding with images and optional audio files.
    Requires Firebase authentication token in the Authorization header.
    """
    # Extract user ID from the decoded token
    user_uid = decoded_token["uid"]
    tasks_goals = await makeprofile(db, user_uid, audios, images)
    return tasks_goals
