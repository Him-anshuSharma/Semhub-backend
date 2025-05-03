from db.services.db_services import session as db  
from db.models.sqlalchemy_models import Subtask, Task, User

# Sync version (recommended if using standard SQLAlchemy)
def add_subtask(subtask: Subtask, task: Task):
    subtask.task = task
    db.add(subtask)
    db.commit()
    db.refresh(subtask)
    return subtask

def get_subtask_by_id(subtask_id: int):   
    return db.query(Subtask).filter(Subtask.id == subtask_id).first()

def update_subtask(subtask: Subtask):
    db.commit()
    db.refresh(subtask)
    return subtask

def delete_subtask(subtask: Subtask):
    db.delete(subtask)
    db.commit()
    return subtask

def get_subtasks_by_user_id(user_id: int):
    return db.query(Subtask).filter(Subtask.user_id == user_id).all()

def get_subtasks_by_user_id_and_status(user_id: int, status: str):    
    return db.query(Subtask).filter(
        Subtask.user_id == user_id,
        Subtask.status == status
    ).all()

def get_subtasks_by_user_id_and_type(user_id: int, subtask_type: str):
    return db.query(Subtask).filter(
        Subtask.user_id == user_id,
        Subtask.subtask_type == subtask_type
    ).all()
