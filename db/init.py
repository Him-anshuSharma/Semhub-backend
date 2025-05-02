import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.sqlalchemy_onboarding import Base


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

def get_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()