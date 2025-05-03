# init.py

from app.init_app import initialize_app, initialize_firebase
from db.init_db import initialize_database, initialize_database

def initialize_services():
    initialize_database()
    initialize_firebase()
    initialize_app()

def get_db_engine():
    from db.init_db import get_engine
    return get_engine()
