# models/models.py
from pydantic import BaseModel
from typing import List, Optional

from db.models.sqlalchemy_models import TaskStatus

class Subtask(BaseModel):
    id: Optional[int] = None
    title: str
    estimated_hours: Optional[float] = None

    class Config:
        orm_mode = True

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    type: str
    subject: str
    deadline: Optional[str] = None
    priority: Optional[str] = None
    estimated_hours: Optional[str] = None
    subtasks: List[Subtask] = []
    status: Optional[str] = TaskStatus.NOT_STARTED.value

    class Config:
        orm_mode = True

class Goal(BaseModel):
    id: Optional[int] = None
    name: str
    type: str
    target_tasks: List[str]  # Stores task IDs as integers
    target_date: Optional[str] = None

    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    firebase_uid: str

    class Config:
        orm_mode = True

class ScreenUsage(BaseModel):
    date: str  # ISO format datetime string
    screen_time: float
    app_name: str
    app_category: str

    class Config:
        orm_mode = True

class Performance(BaseModel):
    date: str  # ISO format datetime string
    performance_score: float

    class Config:
        orm_mode = True

class Response(BaseModel):
    tasks: List[Task]
    goals: List[Goal]

    class Config:
        orm_mode = True
