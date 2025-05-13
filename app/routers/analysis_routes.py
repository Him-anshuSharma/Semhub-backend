from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from app.services.analysis_services import DataAnalyzer
from db.init_db import get_session as get_db  # Replace with your actual get_db function

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/task-statistics/{user_id}")
async def get_task_statistics(user_id: str, db: Session = Depends(get_db)):
    """
    Returns statistics about the user's tasks.
    """
    analyzer = DataAnalyzer(db)
    return analyzer.get_user_task_statistics(user_id)

@router.get("/goal-progress/{user_id}")
async def get_goal_progress(user_id: str, db: Session = Depends(get_db)):
    """
    Returns progress on the user's goals.
    """
    analyzer = DataAnalyzer(db)
    return analyzer.get_user_goal_progress(user_id)

@router.get("/screen-usage/{user_id}")
async def get_screen_usage(
    user_id: str, 
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Returns analysis of screen usage over the past N days (default: 7).
    """
    analyzer = DataAnalyzer(db)
    return analyzer.get_screen_usage_analysis(user_id, days)

@router.get("/performance/{user_id}")
async def get_performance(
    user_id: str, 
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Returns performance metrics over the past N days (default: 30).
    """
    analyzer = DataAnalyzer(db)
    return analyzer.get_performance_metrics(user_id, days)

@router.get("/task-trends/{user_id}")
async def get_task_trends(
    user_id: str, 
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Returns task completion trends over the past N days (default: 30).
    """
    analyzer = DataAnalyzer(db)
    return analyzer.get_task_completion_trends(user_id, days)

@router.get("/predict-task-completion-time/{user_id}")
async def predict_task_completion_time(user_id: str, db: Session = Depends(get_db)):
    """
    Predicts task completion time for the user using ML.
    """
    analyzer = DataAnalyzer(db)
    result = analyzer.predict_task_completion_time(user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/predict-performance-trend/{user_id}")
async def predict_performance_trend(user_id: str, db: Session = Depends(get_db)):
    """
    Predicts performance trend for the user using ML.
    """
    analyzer = DataAnalyzer(db)
    result = analyzer.predict_performance_trend(user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/analyze-screen-usage-patterns/{user_id}")
async def analyze_screen_usage_patterns(user_id: str, db: Session = Depends(get_db)):
    """
    Analyzes screen usage patterns for the user using ML.
    """
    analyzer = DataAnalyzer(db)
    result = analyzer.analyze_screen_usage_patterns(user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/ml-insights/{user_id}")
async def get_ml_insights(user_id: str, db: Session = Depends(get_db)):
    """
    Returns all ML-based insights for the user.
    """
    analyzer = DataAnalyzer(db)
    result = analyzer.get_ml_insights(user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
