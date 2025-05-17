from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.verify_firebase_token import verify_firebase_token as get_user_id
from app.models.pydantic_models import Task
from db.services.user_services import get_user_by_firebase_id
import app.services.pydantic_map_sqlalchemy as model_map
from db.services.task_services import (
    add_task,
    get_task_by_id,
    update_task,
    delete_task,
    get_tasks_by_user_id,
    get_tasks_by_user_id_and_status,
    get_tasks_by_user_id_and_type,
    get_tasks_by_user_id_and_goal_id
)
from db.init_db import get_session as get_db

router = APIRouter(prefix="/task", tags=["Task"])

# Create Task
@router.post("/add-task", response_model=Task)
async def add_task_route(task: Task, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        orm_task = model_map.pydantic_task_to_orm(task)
        db_task = add_task(orm_task, user, db)
        return model_map.orm_task_to_pydantic(db_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Single Task
@router.get("/get-task/{task_id}", response_model=Task)
async def get_task_route(task_id: int, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        task = get_task_by_id(task_id, db)
        if not task or task.user_id != user.id:
            raise HTTPException(status_code=404, detail="Task not found")
            
        return model_map.orm_task_to_pydantic(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update Task
@router.put("/update-task/{task_id}", response_model=Task)
async def update_task_route(task_id: int, task: Task, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        existing_task = get_task_by_id(task_id, db)
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
            
        if existing_task.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")
        
        # Update the existing task's fields
        existing_task.title = task.title
        existing_task.type = task.type
        existing_task.subject = task.subject
        existing_task.deadline = task.deadline
        existing_task.priority = task.priority
        existing_task.estimated_hours = task.estimated_hours
        
        # Update subtasks
        existing_task.subtasks = [
            model_map.pydantic_subtask_to_orm(st, task_id) for st in task.subtasks
        ]
        
        updated_task = update_task(existing_task, db)
        return model_map.orm_task_to_pydantic(updated_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete Task
@router.delete("/delete-task/{task_id}")
async def delete_task_route(task_id: int, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        task = get_task_by_id(task_id, db)
        if not task or task.user_id != user.id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        delete_task(task, db)
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get All Tasks for User
@router.get("/get-tasks", response_model=list[Task])
async def get_tasks(user_id: str, db: Session = Depends(get_db)):
    try:
        uid = await get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tasks = get_tasks_by_user_id(user.id, db)
        return [model_map.orm_task_to_pydantic(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional Filter Endpoints
@router.get("/tasks-by-status/{status}", response_model=list[Task])
async def get_tasks_by_status_route(status: str, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tasks = get_tasks_by_user_id_and_status(user.id, status, db)
        return [model_map.orm_task_to_pydantic(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks-by-type/{task_type}", response_model=list[Task])
async def get_tasks_by_type_route(task_type: str, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tasks = get_tasks_by_user_id_and_type(user.id, task_type, db)
        return [model_map.orm_task_to_pydantic(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks-by-goal/{goal_id}", response_model=list[Task])
async def get_tasks_by_goal_route(goal_id: int, user_id: str, db: Session = Depends(get_db)):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tasks = get_tasks_by_user_id_and_goal_id(user.id, goal_id, db)
        return [model_map.orm_task_to_pydantic(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
