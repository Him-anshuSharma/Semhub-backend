from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.verify_firebase_token import verify_firebase_token as get_user_id
from app.models.pydantic_models import Goal, Task
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
from db.init_db import get_session as get_db

router = APIRouter(prefix="/goal", tags=["Goal"])

#create goal
@router.post("/add-goal", response_model=Goal)
async def addGoal(goal: Goal, user_id: str, db: Session = Depends(get_db)):
    orm_goal = model_map.pydantic_goal_to_orm(goal)
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        for task_name in goal.target_tasks:
            task = get_task_by_user_id_and_task_title(uid, task_name)
            if not task:
                task = Task(title=task_name, type=goal.type, subject=goal.name)
                orm_task = model_map.pydantic_task_to_orm(task)
                if add_task(orm_task, user):
                    orm_goal.target_tasks.append(orm_task)
                else:
                    HTTPException(status_code=400, detail="Failed to add task")
        res = add_goal(orm_goal, user)
        if not res:
            raise HTTPException(status_code=400, detail="Failed to add goal")
        return goal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_goal/{goal_id}", response_model=Goal)
async def getGoal(goal_id: str, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        goal = get_goal_by_id(goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return goal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update-goal/{goal_id}", response_model=Goal)
async def updateGoal(goal_id: str, goal: Goal, user_id: str, db: Session = Depends(get_db)):
    orm_goal = model_map.pydantic_goal_to_orm(goal)
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        existing_goal = get_goal_by_id(goal_id)
        if not existing_goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return update_goal(goal_id, orm_goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-goal/{goal_id}")
async def deleteGoal(goal_id: str, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        existing_goal = get_goal_by_id(goal_id)
        if not existing_goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        delete_goal(goal_id)
        return {"message": "Goal deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-goals", response_model=list[Goal])
async def getGoals(user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        goals = get_goals_by_user_id(user.id)
        pydantic_goals = [model_map.orm_goal_to_pydantic(goal) for goal in goals]
        return pydantic_goals
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

