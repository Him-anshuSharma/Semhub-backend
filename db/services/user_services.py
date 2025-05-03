from db.services.db_services import session
from db.models.sqlalchemy_models import User

def add_user(user):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_firebase_id(firebase_id) -> User:
    return session.query(User).filter(User.firebase_uid == firebase_id).first()

def update_user(user):
    session.commit()
    session.refresh(user)
    return user

def delete_user(user):      
    session.delete(user)
    session.commit()
    return user







