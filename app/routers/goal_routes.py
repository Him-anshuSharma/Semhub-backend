from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.verify_firebase_token import verify_firebase_token as get_user_id
from app.models.pydantic_models import Goal, Task, TaskReference
from db.services.user_services import get_user_by_firebase_id
import app.services.pydantic_map_sqlalchemy as model_map
from db.services.goal_services import (
    add_goal,
    get_goal_by_id,
    update_goal,
    delete_goal,
    get_goals_by_user_id,
)
from db.services.task_services import add_task, get_task_by_id
from db.models.sqlalchemy_models import Task as DbTask
from db.init_db import get_session as get_db

router = APIRouter(prefix="/goal", tags=["Goal"])

@router.post("/add-goal", response_model=Goal)
async def addGoal(goal: Goal, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = await get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert Pydantic goal to ORM goal
        orm_goal = model_map.pydantic_goal_to_orm(goal)
        
        # Process each task reference
        for task_ref in goal.target_tasks:
            task = get_task_by_id(task_ref.id, db) if task_ref.id else None
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

@router.get("/get-goal/{goal_id}", response_model=Goal)
async def getGoal(goal_id: int, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = await get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        goal = get_goal_by_id(db, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        if goal.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this goal")
            
        return model_map.orm_goal_to_pydantic(goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update-goal/{goal_id}", response_model=Goal)
async def updateGoal(goal_id: int, goal: Goal, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = await get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        existing_goal = get_goal_by_id(db, goal_id)
        if not existing_goal:
            raise HTTPException(status_code=404, detail="Goal not found")
            
        if existing_goal.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this goal")

        # Update existing goal's tasks
        existing_goal.target_tasks = []
        for task_ref in goal.target_tasks:
            task = get_task_by_id(task_ref.id, db) if task_ref.id else None
            if not task:
                new_task = DbTask(
                    title=task_ref.title,
                    type=goal.type,
                    subject=goal.name
                )
                task = add_task(new_task, user, db)
            existing_goal.target_tasks.append(task)

        # Update other fields
        existing_goal.name = goal.name
        existing_goal.type = goal.type
        existing_goal.target_date = goal.target_date
        
        updated_goal = update_goal(db, existing_goal)
        return model_map.orm_goal_to_pydantic(updated_goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-goal/{goal_id}")
async def deleteGoal(goal_id: int, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = await get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        goal = get_goal_by_id(db, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
            
        if goal.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this goal")
        
        delete_goal(db, goal)
        return {"message": "Goal deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-goals", response_model=list[Goal])
async def getGoals(user_id: str, db: Session = Depends(get_db)):
    try:
        uid = await get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        goals = get_goals_by_user_id(db, user.id)
        return [model_map.orm_goal_to_pydantic(goal) for goal in goals]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

