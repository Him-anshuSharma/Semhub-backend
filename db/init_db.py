import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.sqlalchemy_models import Base

_engine = None
_SessionLocal = None

def initialize_database():
    global _engine, _SessionLocal
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL not set in environment or .env file!")
    _engine = create_engine(database_url)
    Base.metadata.create_all(bind=_engine)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

def get_engine():
    if _engine is None:
        raise RuntimeError("Database engine not initialized. Call initialize_database() first.")
    return _engine

def get_session():
    if _SessionLocal is None:
        raise RuntimeError("Session maker not initialized. Call initialize_database() first.")
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
