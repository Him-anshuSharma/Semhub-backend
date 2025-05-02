from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, Numeric
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

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
    firebase_uid = Column(String(255), unique=True, nullable=False)  # Firebase user ID
    
    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    subject = Column(String(50), nullable=False)
    priority = Column(String(10), nullable=False)
    deadline = Column(DateTime, nullable=True)
    estimated_hours = Column(Numeric(5,2), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # User association

    # Relationships
    user = relationship("User", back_populates="tasks")
    subtasks = relationship("Subtask", back_populates="task", cascade="all, delete-orphan")
    goals = relationship("Goal", secondary=goal_task_association, backref="tasks")

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
    user_id = Column(Integer, ForeignKey('users.id'))  # User association

    # Relationships
    user = relationship("User", back_populates="goals")
    target_tasks = relationship("Task", secondary=goal_task_association, backref="goals")
