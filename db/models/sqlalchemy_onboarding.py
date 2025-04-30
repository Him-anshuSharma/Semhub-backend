from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between Task and Goal
goal_task_association = Table(
    'goal_task_association',
    Base.metadata,
    Column('goal_id', Integer, ForeignKey('goals.id')),
    Column('task_id', Integer, ForeignKey('tasks.id'))
)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    priority = Column(String, nullable=False)

    # One-to-many: Task has many Subtasks
    subtasks = relationship("Subtask", back_populates="task", cascade="all, delete-orphan")

class Subtask(Base):
    __tablename__ = 'subtasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task", back_populates="subtasks")

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    # Many-to-many: Goal has many Tasks
    target_tasks = relationship(
        "Task",
        secondary=goal_task_association,
        backref="goals"
    )
