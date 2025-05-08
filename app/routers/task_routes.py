from fastapi import APIRouter, HTTPException

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

router = APIRouter(prefix="/task", tags=["Task"])

# Create Task
@router.post("/add-task", response_model=Task)
async def add_task_route(task: Task, user_id: str):
    orm_task = model_map.pydantic_task_to_orm(task)
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return add_task(orm_task, user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Single Task
@router.get("/get-task/{task_id}", response_model=Task)
async def get_task_route(task_id: int, user_id: str):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        task = get_task_by_id(task_id)
        if not task or task.user_id != user.id:
            raise HTTPException(status_code=404, detail="Task not found")
            
        return model_map.orm_task_to_pydantic(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update Task
@router.put("/update-task/{task_id}", response_model=Task)
async def update_task_route(task_id: int, task: Task, user_id: str):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        existing_task = get_task_by_id(task_id)
        if not existing_task or existing_task.user_id != user.id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        updated_task = update_task(model_map.pydantic_task_to_orm(task))
        return model_map.orm_task_to_pydantic(updated_task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete Task
@router.delete("/delete-task/{task_id}")
async def delete_task_route(task_id: int, user_id: str):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        task = get_task_by_id(task_id)
        if not task or task.user_id != user.id:
            raise HTTPException(status_code=404, detail="Task not found")
        
        delete_task(task)
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get All Tasks for User
@router.get("/get-tasks", response_model=list[Task])
async def get_tasks_route(user_id: str):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tasks = get_tasks_by_user_id(user.id)
        return [model_map.orm_task_to_pydantic(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional Filter Endpoints
@router.get("/tasks-by-status/{status}", response_model=list[Task])
async def get_tasks_by_status_route(status: str, user_id: str):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tasks = get_tasks_by_user_id_and_status(user.id, status)
        return [model_map.orm_task_to_pydantic(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks-by-type/{task_type}", response_model=list[Task])
async def get_tasks_by_type_route(task_type: str, user_id: str):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tasks = get_tasks_by_user_id_and_type(user.id, task_type)
        return [model_map.orm_task_to_pydantic(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks-by-goal/{goal_id}", response_model=list[Task])
async def get_tasks_by_goal_route(goal_id: int, user_id: str):
    try:
        uid = get_user_id(user_id)
        user = get_user_by_firebase_id(uid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tasks = get_tasks_by_user_id_and_goal_id(user.id, goal_id)
        return [model_map.orm_task_to_pydantic(task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
