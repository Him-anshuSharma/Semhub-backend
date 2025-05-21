from app.models.pydantic_models import Task as PydanticTask, Subtask as PydanticSubtask, Goal as PydanticGoal, Response as PydanticResponse, User as PydanticUser, ScreenUsage as PydanticScreenUsage, Performance as PydanticPerformance
from typing import List
from datetime import datetime

from db.models.sqlalchemy_models import Task, Subtask, Goal, User, ScreenUsage, Performance  # Adjust import as needed

def orm_subtask_to_pydantic(subtask: Subtask) -> PydanticSubtask:
    return PydanticSubtask(
        id=subtask.id,  # Added ID
        title=subtask.title,
        estimated_hours=float(subtask.estimated_hours) if subtask.estimated_hours is not None else None
    )

def orm_task_to_pydantic(task: Task) -> PydanticTask:
    return PydanticTask(
        id=task.id,  # Added ID
        title=task.title,
        type=task.type,
        subject=task.subject,
        deadline=task.deadline.isoformat() if task.deadline else None,
        priority=task.priority,
        estimated_hours=str(task.estimated_hours) if task.estimated_hours is not None else None,
        subtasks=[orm_subtask_to_pydantic(st) for st in task.subtasks]
    )

def orm_goal_to_pydantic(goal: Goal) -> PydanticGoal:
    return PydanticGoal(
        id=goal.id,  # Added ID
        name=goal.name,  # Using name field until database migration is done
        type=goal.type,
        target_tasks=[str(task.id) for task in goal.target_tasks],  # Just pass the task IDs as strings
        target_date=goal.target_date.isoformat() if goal.target_date else None
    )


def orm_user_to_pydantic(user: User) -> PydanticUser:
    return PydanticUser(
        id=user.id,
        firebase_uid=user.firebase_uid
    )

def orm_screenusage_to_pydantic(screen_usage: ScreenUsage) -> PydanticScreenUsage:
    return PydanticScreenUsage(
        date=screen_usage.date.isoformat() if screen_usage.date else None,
        screen_time=float(screen_usage.screen_time),
        app_name=screen_usage.app_name,
        app_category=screen_usage.app_category
    )

def orm_performance_to_pydantic(performance: Performance) -> PydanticPerformance:
    return PydanticPerformance(
        date=performance.date.isoformat() if performance.date else None,
        performance_score=float(performance.performance_score)
    )

def pydantic_subtask_to_orm(subtask: PydanticSubtask, task_id: int = None) -> Subtask:
    return Subtask(
        title=subtask.title,
        estimated_hours=subtask.estimated_hours,
        task_id=task_id
    )

def pydantic_task_to_orm(task: PydanticTask, user_id: int = None) -> Task:
    orm_task = Task(
        title=task.title,
        type=task.type,
        subject=task.subject,
        deadline=datetime.fromisoformat(task.deadline) if task.deadline else None,
        priority=task.priority,
        estimated_hours=float(task.estimated_hours) if task.estimated_hours else None,
        user_id=user_id
    )
    orm_task.subtasks = [pydantic_subtask_to_orm(st) for st in task.subtasks]
    return orm_task

def pydantic_goal_to_orm(goal: PydanticGoal, user_id: int = None, tasks: List[Task] = None) -> Goal:
    orm_goal = Goal(
        name=goal.name,
        type=goal.type,
        target_date=datetime.fromisoformat(goal.target_date).isoformat().replace('+00:00', 'Z') if goal.target_date else None,
        user_id=user_id
    )
    if tasks:
        orm_goal.target_tasks = tasks
    return orm_goal

def pydantic_user_to_orm(user: PydanticUser) -> User:
    return User(
        id=user.id,
        firebase_uid=user.firebase_uid
    )

def pydantic_screenusage_to_orm(screen_usage: PydanticScreenUsage, user_id: int) -> ScreenUsage:
    return ScreenUsage(
        user_id=user_id,
        date=datetime.fromisoformat(screen_usage.date) if screen_usage.date else None,
        screen_time=screen_usage.screen_time,
        app_name=screen_usage.app_name,
        app_category=screen_usage.app_category
    )

def pydantic_performance_to_orm(performance: PydanticPerformance, task_id: int) -> Performance:
    return Performance(
        date=datetime.fromisoformat(performance.date) if performance.date else None,
        performance_score=performance.performance_score,
        task_id=task_id
    )

def orm_response_to_pydantic(tasks: List[Task], goals: List[Goal]) -> PydanticResponse:
    return PydanticResponse(
        tasks=[orm_task_to_pydantic(task) for task in tasks],
        goals=[orm_goal_to_pydantic(goal) for goal in goals]
    )
