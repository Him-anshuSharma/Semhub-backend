from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from db.models.sqlalchemy_models import (
    Task, Goal, ScreenUsage, Performance
)

class DataAnalyzer:
    def __init__(self, session):
        self.session = session
        self.task_completion_model = None
        self.performance_prediction_model = None
        self.screen_usage_model = None
        self.label_encoders = {}

    def get_user_task_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive statistics about a user's tasks."""
        tasks = self.session.query(Task).filter(Task.user_id == user_id).all()
        
        stats = {
            "total_tasks": len(tasks),
            "completed_tasks": len([t for t in tasks if t.completed_at is not None]),
            "pending_tasks": len([t for t in tasks if t.completed_at is None]),
            "tasks_by_type": {},
            "tasks_by_subject": {},
            "average_estimated_hours": 0,
            "total_estimated_hours": 0
        }

        total_hours = 0
        for task in tasks:
            # Count by type
            stats["tasks_by_type"][task.type] = stats["tasks_by_type"].get(task.type, 0) + 1
            # Count by subject
            stats["tasks_by_subject"][task.subject] = stats["tasks_by_subject"].get(task.subject, 0) + 1
            # Sum estimated hours
            if task.estimated_hours:
                total_hours += float(task.estimated_hours)

        if tasks:
            stats["average_estimated_hours"] = total_hours / len(tasks)
            stats["total_estimated_hours"] = total_hours

        return stats

    def get_user_goal_progress(self, user_id: int) -> List[Dict[str, Any]]:
        """Get progress of all goals for a user."""
        goals = self.session.query(Goal).filter(Goal.user_id == user_id).all()
        
        goal_progress = []
        for goal in goals:
            total_tasks = len(goal.target_tasks)
            completed_tasks = len([t for t in goal.target_tasks if t.completed_at is not None])
            
            progress = {
                "goal_id": goal.id,
                "name": goal.name,
                "type": goal.type,
                "target_date": goal.target_date,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
            goal_progress.append(progress)
        
        return goal_progress

    def get_screen_usage_analysis(self, user_id: int, days: int = 7) -> Dict[str, Any]:
        """Analyze screen usage patterns for a user over the specified number of days."""
        start_date = datetime.now() - timedelta(days=days)
        
        usage_data = self.session.query(ScreenUsage).filter(
            and_(
                ScreenUsage.user_id == user_id,
                ScreenUsage.date >= start_date
            )
        ).all()

        analysis = {
            "total_screen_time": 0,
            "daily_average": 0,
            "app_usage": {},
            "category_usage": {},
            "daily_breakdown": {}
        }

        for usage in usage_data:
            # Convert to float for calculations
            screen_time = float(usage.screen_time)
            
            # Update total screen time
            analysis["total_screen_time"] += screen_time
            
            # Update app usage
            analysis["app_usage"][usage.app_name] = analysis["app_usage"].get(usage.app_name, 0) + screen_time
            
            # Update category usage
            analysis["category_usage"][usage.app_category] = analysis["category_usage"].get(usage.app_category, 0) + screen_time
            
            # Update daily breakdown
            date_str = usage.date.strftime("%Y-%m-%d")
            analysis["daily_breakdown"][date_str] = analysis["daily_breakdown"].get(date_str, 0) + screen_time

        # Calculate daily average
        if usage_data:
            analysis["daily_average"] = analysis["total_screen_time"] / len(set(u.date for u in usage_data))

        return analysis

    def get_performance_metrics(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get performance metrics for a user's tasks."""
        start_date = datetime.now() - timedelta(days=days)
        
        performances = self.session.query(Performance).join(Task).filter(
            and_(
                Task.user_id == user_id,
                Performance.date >= start_date
            )
        ).all()

        metrics = {
            "average_score": 0,
            "total_tasks_analyzed": len(performances),
            "score_distribution": {
                "excellent": 0,  # 90-100
                "good": 0,      # 70-89
                "average": 0,   # 50-69
                "poor": 0       # 0-49
            },
            "daily_scores": {}
        }

        if performances:
            total_score = sum(float(p.performance_score) for p in performances)
            metrics["average_score"] = total_score / len(performances)

            for perf in performances:
                score = float(perf.performance_score)
                
                # Update score distribution
                if score >= 90:
                    metrics["score_distribution"]["excellent"] += 1
                elif score >= 70:
                    metrics["score_distribution"]["good"] += 1
                elif score >= 50:
                    metrics["score_distribution"]["average"] += 1
                else:
                    metrics["score_distribution"]["poor"] += 1
                
                # Update daily scores
                date_str = perf.date.strftime("%Y-%m-%d")
                if date_str not in metrics["daily_scores"]:
                    metrics["daily_scores"][date_str] = []
                metrics["daily_scores"][date_str].append(score)

        return metrics

    def get_task_completion_trends(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Analyze task completion trends over time."""
        start_date = datetime.now() - timedelta(days=days)
        
        tasks = self.session.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.created_at >= start_date
            )
        ).all()

        trends = {
            "completion_rate": 0,
            "average_completion_time": 0,
            "daily_completions": {},
            "type_completion_rates": {},
            "subject_completion_rates": {}
        }

        completed_tasks = [t for t in tasks if t.completed_at is not None]
        total_completion_time = 0

        for task in completed_tasks:
            # Calculate completion time in hours
            if task.started_at and task.completed_at:
                completion_time = (task.completed_at - task.started_at).total_seconds() / 3600
                total_completion_time += completion_time

            # Update daily completions
            date_str = task.completed_at.strftime("%Y-%m-%d")
            trends["daily_completions"][date_str] = trends["daily_completions"].get(date_str, 0) + 1

            # Update type completion rates
            if task.type not in trends["type_completion_rates"]:
                trends["type_completion_rates"][task.type] = {"completed": 0, "total": 0}
            trends["type_completion_rates"][task.type]["completed"] += 1

            # Update subject completion rates
            if task.subject not in trends["subject_completion_rates"]:
                trends["subject_completion_rates"][task.subject] = {"completed": 0, "total": 0}
            trends["subject_completion_rates"][task.subject]["completed"] += 1

        # Calculate overall completion rate
        if tasks:
            trends["completion_rate"] = len(completed_tasks) / len(tasks) * 100

        # Calculate average completion time
        if completed_tasks:
            trends["average_completion_time"] = total_completion_time / len(completed_tasks)

        # Calculate completion rates for types and subjects
        for task in tasks:
            if task.type not in trends["type_completion_rates"]:
                trends["type_completion_rates"][task.type] = {"completed": 0, "total": 0}
            trends["type_completion_rates"][task.type]["total"] += 1

            if task.subject not in trends["subject_completion_rates"]:
                trends["subject_completion_rates"][task.subject] = {"completed": 0, "total": 0}
            trends["subject_completion_rates"][task.subject]["total"] += 1

        return trends

    def prepare_task_features(self, tasks: List[Task]) -> np.ndarray:
        """Prepare features for task-related ML models."""
        features = []
        for task in tasks:
            # Convert categorical variables using label encoders
            if 'type' not in self.label_encoders:
                self.label_encoders['type'] = LabelEncoder()
                self.label_encoders['type'].fit([t.type for t in tasks])
            if 'subject' not in self.label_encoders:
                self.label_encoders['subject'] = LabelEncoder()
                self.label_encoders['subject'].fit([t.subject for t in tasks])
            
            type_encoded = self.label_encoders['type'].transform([task.type])[0]
            subject_encoded = self.label_encoders['subject'].transform([task.subject])[0]
            
            # Create feature vector
            feature_vector = [
                type_encoded,
                subject_encoded,
                float(task.estimated_hours) if task.estimated_hours else 0,
                (task.deadline - task.created_at).total_seconds() / 3600 if task.deadline else 0,
                len(task.subtasks),
                task.priority == 'high' if task.priority else 0
            ]
            features.append(feature_vector)
        return np.array(features)

    def predict_task_completion_time(self, user_id: int) -> Dict[str, Any]:
        """Predict completion time for new tasks using ML model."""
        # Get historical completed tasks
        completed_tasks = self.session.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.completed_at.isnot(None),
                Task.started_at.isnot(None)
            )
        ).all()

        if len(completed_tasks) < 10:  # Need minimum data for training
            return {"error": "Insufficient historical data for prediction"}

        # Prepare features and target
        X = self.prepare_task_features(completed_tasks)
        y = np.array([(t.completed_at - t.started_at).total_seconds() / 3600 for t in completed_tasks])

        # Split data and train model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        if self.task_completion_model is None:
            self.task_completion_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        self.task_completion_model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.task_completion_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        
        return {
            "model_accuracy": 1 - (mse / np.mean(y_test)),
            "feature_importance": dict(zip(
                ['type', 'subject', 'estimated_hours', 'deadline_hours', 'subtask_count', 'high_priority'],
                self.task_completion_model.feature_importances_
            ))
        }

    def predict_performance_trend(self, user_id: int) -> Dict[str, Any]:
        """Predict future performance trends using ML model."""
        # Get historical performance data
        performances = self.session.query(Performance).join(Task).filter(
            Task.user_id == user_id
        ).order_by(Performance.date).all()

        if len(performances) < 10:
            return {"error": "Insufficient historical data for prediction"}

        # Prepare features (using time-based features)
        X = np.array([[i] for i in range(len(performances))])
        y = np.array([float(p.performance_score) for p in performances])

        # Split data and train model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        if self.performance_prediction_model is None:
            self.performance_prediction_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        self.performance_prediction_model.fit(X_train, y_train)
        
        # Predict next 7 days
        future_days = np.array([[len(performances) + i] for i in range(7)])
        future_predictions = self.task_completion_model.predict(future_days)
        
        return {
            "predicted_trend": list(future_predictions),
            "confidence_score": self.performance_prediction_model.score(X_test, y_test)
        }

    def analyze_screen_usage_patterns(self, user_id: int) -> Dict[str, Any]:
        """Analyze screen usage patterns using ML clustering."""
        # Get screen usage data
        usage_data = self.session.query(ScreenUsage).filter(
            ScreenUsage.user_id == user_id
        ).order_by(ScreenUsage.date).all()

        if len(usage_data) < 10:
            return {"error": "Insufficient historical data for analysis"}

        # Prepare features
        features = []
        for usage in usage_data:
            feature_vector = [
                usage.date.hour,  # Hour of day
                usage.date.weekday(),  # Day of week
                float(usage.screen_time),
                1 if usage.app_category == 'productivity' else 0,
                1 if usage.app_category == 'social' else 0,
                1 if usage.app_category == 'entertainment' else 0
            ]
            features.append(feature_vector)

        X = np.array(features)
        
        # Train model to predict screen time
        if self.screen_usage_model is None:
            self.screen_usage_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Use screen time as target
        y = X[:, 2]  # screen_time column
        X = np.delete(X, 2, axis=1)  # Remove screen_time from features
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.screen_usage_model.fit(X_train, y_train)
        
        # Analyze patterns
        feature_importance = dict(zip(
            ['hour_of_day', 'day_of_week', 'is_productivity', 'is_social', 'is_entertainment'],
            self.screen_usage_model.feature_importances_
        ))
        
        # Predict optimal usage times
        optimal_times = []
        for hour in range(24):
            for day in range(7):
                prediction = self.screen_usage_model.predict([[hour, day, 1, 0, 0]])[0]
                if prediction < 2:  # Less than 2 hours is considered optimal
                    optimal_times.append({
                        "hour": hour,
                        "day": day,
                        "predicted_usage": float(prediction)
                    })
        
        return {
            "feature_importance": feature_importance,
            "optimal_usage_times": optimal_times,
            "model_accuracy": self.screen_usage_model.score(X_test, y_test)
        }

    def get_ml_insights(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive ML-based insights for a user."""
        completion_prediction = self.predict_task_completion_time(user_id)
        performance_trend = self.predict_performance_trend(user_id)
        screen_patterns = self.analyze_screen_usage_patterns(user_id)
        
        return {
            "task_completion_prediction": completion_prediction,
            "performance_trend_prediction": performance_trend,
            "screen_usage_patterns": screen_patterns
        } 