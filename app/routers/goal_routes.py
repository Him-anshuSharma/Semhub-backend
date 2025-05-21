from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.verify_firebase_token import get_verified_user_id
from app.models.pydantic_models import Goal
from db.services.user_services import get_user_by_firebase_id
import app.services.pydantic_map_sqlalchemy as model_map
from db.services.goal_services import (
    add_goal,
    get_goal_by_id,
    update_goal,
    delete_goal,
    get_goals_by_user_id,
)
from db.services.task_services import add_task, get_task_by_user_id_and_task_title
from db.models.sqlalchemy_models import Task as DbTask
from db.init_db import get_session as get_db

router = APIRouter(prefix="/goal", tags=["Goal"])

@router.post("/add-goal", response_model=Goal)
async def addGoal(
    goal: Goal,
    user_id: str = Depends(get_verified_user_id),
    db: Session = Depends(get_db)
):
    """
    Create a new goal.
    Requires Firebase authentication token in the Authorization header.
    """
    try:
        user = get_user_by_firebase_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert Pydantic goal to ORM goal
        orm_goal = model_map.pydantic_goal_to_orm(goal)
        
        # Process each task reference
        for task_ref in goal.target_tasks:
            task = get_task_by_user_id_and_task_title(
                user.id, task_ref.title, db
            )
            if not task:
                new_task = DbTask(
                    title=task_ref.title,
                    type=goal.type,
                    subject=goal.name
                )
                task = add_task(new_task, user, db)
            orm_goal.target_tasks.append(task)

        # Add goal to database
        db_goal = add_goal(db, orm_goal, user)
        if not db_goal:
            raise HTTPException(status_code=400, detail="Failed to add goal")
        
        return model_map.orm_goal_to_pydantic(db_goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_goal/{goal_id}", response_model=Goal)
async def getGoal(goal_id: str, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_verified_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        goal = get_goal_by_id(goal_id, db)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return model_map.orm_goal_to_pydantic(goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update-goal/{goal_id}", response_model=Goal)
async def updateGoal(goal_id: str, goal: Goal, user_id: str, db: Session = Depends(get_db)):
    orm_goal = model_map.pydantic_goal_to_orm(goal)
    try:
        uid = get_verified_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        existing_goal = get_goal_by_id(goal_id, db)
        if not existing_goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        updated_goal = update_goal(goal_id, orm_goal, db)
        return model_map.orm_goal_to_pydantic(updated_goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-goal/{goal_id}")
async def deleteGoal(
    goal_id: int,  # Changed type to int
    user_id: str = Depends(get_verified_user_id),  # Added token verification
    db: Session = Depends(get_db)
):
    try:
        user = get_user_by_firebase_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Get goal and verify ownership
        goal = get_goal_by_id(goal_id, db)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        if goal.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this goal")
            
        delete_goal(goal_id, db)
        return {
            "success": True,
            "message": "Goal deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-goals", response_model=list[Goal])
async def getGoals(user_id: str = Depends(get_verified_user_id), db: Session = Depends(get_db)):
    try:
        user = get_user_by_firebase_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # Fix: Pass db first, then user.id
        goals = get_goals_by_user_id(db, user.id)
        pydantic_goals = [model_map.orm_goal_to_pydantic(goal) for goal in goals]
        return pydantic_goals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

