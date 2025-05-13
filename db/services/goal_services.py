from db.models.sqlalchemy_models import Goal, User
from sqlalchemy.orm import Session

def add_goal(db: Session, goal: Goal, user: User):
    goal.user = user  # Associate goal with the user
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

def get_goal_by_id(db: Session, goal_id: int):
    return db.query(Goal).filter(Goal.id == goal_id).first()

def update_goal(db: Session, goal: Goal):
    db.commit()
    db.refresh(goal)
    return goal

def delete_goal(db: Session, goal: Goal):
    db.delete(goal)
    db.commit()
    return goal

def get_goals_by_user_id(db: Session, user_id: int):
    return db.query(Goal).filter(Goal.user_id == user_id).all()

def get_goals_by_user_id_and_status(db: Session, user_id: int, status: str):   
    return db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.status == status
    ).all()

def get_goals_by_user_id_and_type(db: Session, user_id: int, goal_type: str):  
    return db.query(Goal).filter(
        Goal.user_id == user_id,
        Goal.goal_type == goal_type
    ).all()
