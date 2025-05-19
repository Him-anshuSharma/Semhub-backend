from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.init_db import get_session as get_db
from db.models.sqlalchemy_models import Subtask as SubtaskORM, Task
from app.services.pydantic_map_sqlalchemy import (
    orm_subtask_to_pydantic,
    pydantic_subtask_to_orm,
)
from app.models.pydantic_models import Subtask as PydanticSubtask
from app.services.verify_firebase_token import get_verified_user_id
from db.services.user_services import get_user_by_firebase_id

router = APIRouter(prefix="/subtask", tags=["Subtask"])

@router.get("/subtasks/{subtask_id}", response_model=PydanticSubtask)
async def get_subtask(
    subtask_id: int,
    user_id: str = Depends(get_verified_user_id),
    db: Session = Depends(get_db)
):
    """
    Get a subtask by ID.
    Requires Firebase authentication token in the Authorization header.
    """
    user = get_user_by_firebase_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    subtask_orm = db.query(SubtaskORM).filter(SubtaskORM.id == subtask_id).first()
    if not subtask_orm:
        raise HTTPException(status_code=404, detail="Subtask not found")
    
    # Verify the subtask belongs to a task owned by the user
    if subtask_orm.task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this subtask")
        
    return orm_subtask_to_pydantic(subtask_orm)

@router.post("/subtasks/", response_model=PydanticSubtask)
async def create_subtask(
    subtask: PydanticSubtask,
    user_id: str = Depends(get_verified_user_id),
    db: Session = Depends(get_db)
):
    """
    Create a new subtask.
    Requires Firebase authentication token in the Authorization header.
    """
    user = get_user_by_firebase_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify the parent task exists and belongs to the user
    parent_task = db.query(Task).filter(Task.id == subtask.task_id).first()
    if not parent_task:
        raise HTTPException(status_code=404, detail="Parent task not found")
    if parent_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add subtask to this task")

    subtask_orm = pydantic_subtask_to_orm(subtask)
    db.add(subtask_orm)
    db.commit()
    db.refresh(subtask_orm)
    return orm_subtask_to_pydantic(subtask_orm)

@router.put("/subtasks/{subtask_id}", response_model=PydanticSubtask)
async def update_subtask(
    subtask_id: int,
    updated_subtask: PydanticSubtask,
    user_id: str = Depends(get_verified_user_id),
    db: Session = Depends(get_db)
):
    """
    Update a subtask by ID.
    Requires Firebase authentication token in the Authorization header.
    """
    user = get_user_by_firebase_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    subtask_orm = db.query(SubtaskORM).filter(SubtaskORM.id == subtask_id).first()
    if not subtask_orm:
        raise HTTPException(status_code=404, detail="Subtask not found")

    # Verify the subtask belongs to a task owned by the user
    if subtask_orm.task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this subtask")

    update_data = updated_subtask.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subtask_orm, key, value)
    db.commit()
    db.refresh(subtask_orm)
    return orm_subtask_to_pydantic(subtask_orm)

@router.delete("/subtasks/{subtask_id}")
async def delete_subtask(
    subtask_id: int,
    user_id: str = Depends(get_verified_user_id),
    db: Session = Depends(get_db)
):
    """
    Delete a subtask by ID.
    Requires Firebase authentication token in the Authorization header.
    """
    user = get_user_by_firebase_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    subtask_orm = db.query(SubtaskORM).filter(SubtaskORM.id == subtask_id).first()
    if not subtask_orm:
        raise HTTPException(status_code=404, detail="Subtask not found")

    # Verify the subtask belongs to a task owned by the user
    if subtask_orm.task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this subtask")

    db.delete(subtask_orm)
    db.commit()
    return {"message": "Subtask deleted successfully"}
