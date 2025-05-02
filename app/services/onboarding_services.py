import os
import json
from datetime import datetime
from fastapi import UploadFile, File, HTTPException
from typing import List, Optional

from app.init_app import client
from constants import onboarding_prompt as prompt, gemini_model
from app.models.onboarding_models import Response
from db.init_db import get_session
from app.services.verify_firebase_token import verify_firebase_token
from db.models.sqlalchemy_onboarding import (
    Task as DbTask,
    Subtask as DbSubtask,
    Goal as DbGoal,
    User
)
from db.services.db import add_user, add_goal, add_task, add_subtask

async def makeprofile(
    token: str,
    audios: Optional[List[UploadFile]] = None,
    images: List[UploadFile] = File(...)
):
    # Verify token and get user UID
    user_uid = verify_firebase_token(token)
    if not user_uid:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db_session = get_session()
    user = db_session.query(User).filter_by(firebase_uid=user_uid).first()
    
    if not user:
        # Create new user if not exists
        user = User(firebase_uid=user_uid)
        add_user(user)

    # File handling
    DIR = "tempfiles"
    os.makedirs(DIR, exist_ok=True)
    file_locations = []

    if audios:
        # TODO: Implement audio handling
        print("Audio files received")

    for image in images:
        image_path = os.path.join(DIR, image.filename)
        with open(image_path, "wb") as out_file:
            content = await image.read()
            out_file.write(content)
        file_locations.append(image_path)

    # Generate content
    contents = [prompt]
    for file in file_locations:
        myfile = client.files.upload(file=file)
        contents.append(myfile)

    try:
        response = client.models.generate_content(
            model=gemini_model,
            contents=contents
        )
        json_data = json.loads(response.text.replace("```", "").replace("json", "").strip())
        gemini_response = Response.model_validate(json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

    add_api_response_to_db(gemini_response, user, db_session)
    return gemini_response

def add_api_response_to_db(
    api_response: Response,
    user: User,
    db_session = None
):
    if not db_session:
        db_session = get_session()

    db_tasks = {}
    
    try:
        # Process tasks
        for api_task in api_response.tasks:
            db_task = DbTask(
                title=api_task.title,
                type=api_task.type,
                subject=api_task.subject,
                priority=api_task.priority,
                deadline=datetime.fromisoformat(api_task.deadline) if api_task.deadline else None,
                estimated_hours=float(api_task.estimated_hours) if api_task.estimated_hours else None,
            )
            
            for api_subtask in api_task.subtasks:
                db_subtask = DbSubtask(
                    title=api_subtask.title,
                    estimated_hours=api_subtask.estimated_hours
                )
                db_task.subtasks.append(db_subtask)
            
            add_task(db_task, user)  # Add task to DB
            db_tasks[api_task.title] = db_task

        db_session.flush()  # Generate IDs for relationships

        # Process goals
        for api_goal in api_response.goals:
            db_goal = DbGoal(
                name=api_goal.name,
                type=api_goal.type,
                target_date=datetime.fromisoformat(api_goal.target_date) if api_goal.target_date else None,
                user=user  # Associate with user
            )
            
            for task_title in api_goal.target_tasks:
                if task_title in db_tasks:
                    db_goal.target_tasks.append(db_tasks[task_title])
            
            add_goal(db_goal, user)

        db_session.commit()
        
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
