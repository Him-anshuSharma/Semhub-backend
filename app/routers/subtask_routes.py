from db.services.db_services import session as db
from db.models.sqlalchemy_models import Subtask
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/subtasks/{subtask_id}")
async def get_subtask(subtask_id: int):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    return subtask

@router.post("/subtasks/")
async def create_subtask(subtask: Subtask):
    db.add(subtask)
    db.commit()
    db.refresh(subtask)
    return subtask

@router.put("/subtasks/{subtask_id}")
async def update_subtask(subtask_id: int, updated_subtask: Subtask):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    for key, value in updated_subtask.dict(exclude_unset=True).items():
        setattr(subtask, key, value)
    db.commit()
    db.refresh(subtask)
    return subtask

@router.delete("/subtasks/{subtask_id}")
async def delete_subtask(subtask_id: int):
    subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    db.delete(subtask)
    db.commit()
    return {"message": "Subtask deleted successfully"}