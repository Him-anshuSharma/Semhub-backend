# models/onboarding.py
from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    title: str
    type: str
    subject: str
    priority: str  # Include all fields from JSON
    subtasks: List[str] = []  # Default empty list if needed

class Goal(BaseModel):
    name: str
    type: str
    target_tasks: List[str]

class Response(BaseModel):
    tasks: List[Task]
    goals: List[Goal]
