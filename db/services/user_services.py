from db.models.sqlalchemy_models import User
from sqlalchemy.orm import Session

def add_user(user, db: Session):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_firebase_id(firebase_id, db: Session) -> User:
    return db.query(User).filter(User.firebase_uid == firebase_id).first()

def update_user(user, db: Session):
    db.commit()
    db.refresh(user)
    return user

def delete_user(user, db: Session):      
    db.delete(user)
    db.commit()
    return user







