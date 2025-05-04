from db.services.db_services import session
from db.models.sqlalchemy_models import Task, User

def add_task(task:Task, user:User):
    print("adding user")
    task.user = user  # Associate task with the user
    print("added user")
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_task_by_id(task_id: int):
    return session.query(Task).filter(Task.id == task_id).first()

def get_task_by_user_id_and_task_title(user_id: str, task_title: str):
    return session.query(Task).filter(Task.user_id == user_id, Task.title == task_title).first()

def update_task(task:Task):
    session.commit()
    session.refresh(task)
    return task

def delete_task(task:Task):
    session.delete(task)
    session.commit()
    return task

def get_tasks_by_user_id(user_id: int):
    return session.query(Task).filter(Task.user_id == user_id).all()

def get_tasks_by_user_id_and_status(user_id: int, status: str):
    return session.query(Task).filter(Task.user_id == user_id, Task.status == status).all()

def get_tasks_by_user_id_and_type(user_id: int, task_type: str):
    return session.query(Task).filter(Task.user_id == user_id, Task.task_type == task_type).all()

def get_tasks_by_user_id_and_goal_id(user_id: int, goal_id: int):
    return session.query(Task).filter(Task.user_id == user_id, Task.goal_id == goal_id).all()