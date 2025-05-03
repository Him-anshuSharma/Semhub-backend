from db.services.db_services import session
from db.models.sqlalchemy_models import Task, User

async def add_task(task:Task, user:User):
    task.user = user  # Associate task with the user
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

async def get_task_by_id(task_id: int):
    return session.query(Task).filter(Task.id == task_id).first()

async def update_task(task:Task):
    session.commit()
    session.refresh(task)
    return task

async def delete_task(task:Task):
    session.delete(task)
    session.commit()
    return task

async def get_tasks_by_user_id(user_id: int):
    return session.query(Task).filter(Task.user_id == user_id).all()

async def get_tasks_by_user_id_and_status(user_id: int, status: str):
    return session.query(Task).filter(Task.user_id == user_id, Task.status == status).all()

async def get_tasks_by_user_id_and_type(user_id: int, task_type: str):
    return session.query(Task).filter(Task.user_id == user_id, Task.task_type == task_type).all()

async def get_tasks_by_user_id_and_goal_id(user_id: int, goal_id: int):
    return session.query(Task).filter(Task.user_id == user_id, Task.goal_id == goal_id).all()