from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Numeric
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from enum import Enum

Base = declarative_base()


class TaskStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

# Association table for many-to-many relationship between Task and Goal
goal_task_association = Table(
    'goal_task_association',
    Base.metadata,
    Column('goal_id', Integer, ForeignKey('goals.id')),
    Column('task_id', Integer, ForeignKey('tasks.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String(255), unique=True, nullable=False)
    
    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    screen_usages = relationship("ScreenUsage", back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    subject = Column(String(50), nullable=False)
    priority = Column(String(10), nullable=True)
    deadline = Column(DateTime, nullable=True)
    estimated_hours = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())  # Fixed default
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)  
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String,default=TaskStatus.NOT_STARTED.value)  # Default status set to NOT_STARTED

    # Relationships
    user = relationship("User", back_populates="tasks")
    subtasks = relationship("Subtask", back_populates="task", cascade="all, delete-orphan")
    target_goals = relationship("Goal", secondary=goal_task_association, back_populates="target_tasks")
    performance = relationship("Performance", back_populates="task")

class Subtask(Base):
    __tablename__ = 'subtasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    estimated_hours = Column(Numeric(5,2), nullable=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", back_populates="subtasks")

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    target_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    user = relationship("User", back_populates="goals")
    target_tasks = relationship(
        "Task", 
        secondary=goal_task_association, 
        back_populates="target_goals", 
        cascade="save-update, merge, delete"
        )

class ScreenUsage(Base):
    __tablename__ = 'screenusage'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime)
    screen_time = Column(Numeric(5,2), nullable=False)
    app_name = Column(String(100), nullable=False)
    app_category = Column(String(50), nullable=False)

    user = relationship("User", back_populates="screen_usages")

class Performance(Base):  # Fixed class name capitalization
    __tablename__ = 'performance'
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    performance_score = Column(Numeric(5,2), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    
    task = relationship("Task", back_populates="performance")
