from db.init import get_session

session = get_session()

def add_user(firebase_uid):
    from models import User  # Import your User model
    user = User(firebase_uid=firebase_uid)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def add_goal(goal, user):
    goal.user = user  # Associate goal with the user
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal

def add_task(task, user):
    task.user = user  # Associate task with the user
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def add_subtask(subtask, task):
    subtask.task = task  # Associate subtask with its parent task
    session.add(subtask)
    session.commit()
    session.refresh(subtask)
    return subtask
