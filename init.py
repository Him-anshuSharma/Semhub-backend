# init.py

from app.init_app import initialize_app
from db.init_db import initialize_database, get_engine

def initialize_services():
    initialize_app()
    initialize_database()

def get_db_engine():
    return get_engine()
