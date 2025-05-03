# models/onboarding.py
from pydantic import BaseModel
from typing import List, Optional

class Subtask(BaseModel):
    title: str
    estimated_hours: float = None

class Task(BaseModel):
    title: str
    type: str
    subject: str
    deadline: str = None  # Optional field
    priority: Optional[str]  # Include all fields from JSON
    estimated_hours: str = None  # Optional field
    subtasks: List[Subtask] = []

class Goal(BaseModel):
    name: str
    type: str
    target_tasks: List[str]
    target_date: str = None  # Optional field

class Response(BaseModel):
    tasks: List[Task]
    goals: List[Goal]
