from fastapi import APIRouter, Depends, HTTPException

from services.verify_firebase_token import verify_firebase_token as get_user_id
from app.models.goal import Goal
from db.services.user_services import get_user_by_firebase_id
from db.services.goal_services import (
    add_goal,
    get_goal_by_id,
    update_goal,
    delete_goal,
    get_goals_by_user_id,
    get_goals_by_user_id_and_status,
    get_goals_by_user_id_and_type
)

router = APIRouter()

#create goal
@router.post("/add-goals", response_model=Goal)
async def addGoal(goal: Goal, user_id: str):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return add_goal(goal,user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
