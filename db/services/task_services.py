from db.models.sqlalchemy_models import Task, User
from sqlalchemy.orm import Session

def add_task(task: Task, user: User, db: Session):
    task.user = user  # Associate task with the user
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task_by_id(task_id: int, db: Session):
    return db.query(Task).filter(Task.id == task_id).first()

def get_task_by_user_id_and_task_title(user_id: str, task_title: str, db: Session):
    return db.query(Task).filter(Task.user_id == user_id, Task.title == task_title).first()

def update_task(task: Task, db: Session):
    db.commit()
    db.refresh(task)
    return task

def delete_task(task: Task, db: Session):
    db.delete(task)
    db.commit()
    return task

def get_tasks_by_user_id(user_id: int, db: Session):
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_tasks_by_user_id_and_status(user_id: int, status: str, db: Session):
    return db.query(Task).filter(Task.user_id == user_id, Task.status == status).all()

def get_tasks_by_user_id_and_type(user_id: int, task_type: str, db: Session):
    return db.query(Task).filter(Task.user_id == user_id, Task.task_type == task_type).all()

def get_tasks_by_user_id_and_goal_id(user_id: int, goal_id: int, db: Session):
    return db.query(Task).filter(Task.user_id == user_id, Task.goal_id == goal_id).all()