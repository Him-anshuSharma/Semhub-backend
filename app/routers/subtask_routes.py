from fastapi import APIRouter, HTTPException
from db.services.db_services import session as db
from db.models.sqlalchemy_models import Subtask as SubtaskORM
from app.services.pydantic_map_sqlalchemy import (
    orm_subtask_to_pydantic,
    pydantic_subtask_to_orm,
)
from app.models.pydantic_models import Subtask as PydanticSubtask

router = APIRouter(prefix="/subtask", tags=["Subtask"])

@router.get("/subtasks/{subtask_id}", response_model=PydanticSubtask)
async def get_subtask(subtask_id: int):
    subtask_orm = db.query(SubtaskORM).filter(SubtaskORM.id == subtask_id).first()
    if not subtask_orm:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return orm_subtask_to_pydantic(subtask_orm)

@router.post("/subtasks/", response_model=PydanticSubtask)
async def create_subtask(subtask: PydanticSubtask):
    subtask_orm = pydantic_subtask_to_orm(subtask)
    db.add(subtask_orm)
    db.commit()
    db.refresh(subtask_orm)
    return orm_subtask_to_pydantic(subtask_orm)

@router.put("/subtasks/{subtask_id}", response_model=PydanticSubtask)
async def update_subtask(subtask_id: int, updated_subtask: PydanticSubtask):
    subtask_orm = db.query(SubtaskORM).filter(SubtaskORM.id == subtask_id).first()
    if not subtask_orm:
        raise HTTPException(status_code=404, detail="Subtask not found")
    # Update fields from the Pydantic model
    update_data = updated_subtask.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subtask_orm, key, value)
    db.commit()
    db.refresh(subtask_orm)
    return orm_subtask_to_pydantic(subtask_orm)

@router.delete("/subtasks/{subtask_id}")
async def delete_subtask(subtask_id: int):
    subtask_orm = db.query(SubtaskORM).filter(SubtaskORM.id == subtask_id).first()
    if not subtask_orm:
        raise HTTPException(status_code=404, detail="Subtask not found")
    db.delete(subtask_orm)
    db.commit()
    return {"message": "Subtask deleted successfully"}
