from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.services.onboarding_services import makeprofile
from app.services.verify_firebase_token import verify_firebase_token
from db.init_db import get_session as get_db
import firebase_admin
from firebase_admin import auth
import os

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
    response_data: Response = await makeprofile(db, user_uid, audios, images)
    
    if not response_data:
        raise HTTPException(status_code=400, detail="Failed to process onboarding")
    
    # Convert Pydantic model to dict and handle datetime serialization
    serialized_data = jsonable_encoder(response_data)

    print("onboarding tasks_goals:\n", serialized_data)
    
    return {
        "success": True,
        "message": "Onboarding completed successfully",
        "data": serialized_data
    }
