from db.services.db_services import session as db
from db.models.sqlalchemy_models import Goal, User

def  add_goal( goal: Goal, user: User):
    goal.user = user  # Associate goal with the user
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

def get_goal_by_id( goal_id: int):
    return db.query(Goal).filter(Goal.id == goal_id).first()

def update_goal( goal: Goal):
    db.commit()
    db.refresh(goal)
    return goal

def delete_goal( goal: Goal):
    db.delete(goal)
    db.commit()
    return goal

def get_goals_by_user_id( user_id: int):
    return db.query(Goal).filter(Goal.user_id == user_id).all()

def get_goals_by_user_id_and_status( user_id: int, status: str):   
    return db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.status == status
    ).all()

def get_goals_by_user_id_and_type( user_id: int, goal_type: str):  
    return db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.goal_type == goal_type
    ).all()
