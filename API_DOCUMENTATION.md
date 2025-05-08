# SemHub API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Task Management](#task-management)
3. [Goal Management](#goal-management)
4. [Subtask Management](#subtask-management)
5. [Analysis & Insights](#analysis--insights)
6. [Onboarding](#onboarding)

## Authentication
All endpoints require Firebase authentication. The user's Firebase token should be passed in the request header or as a parameter.

## Task Management

### Create Task
```http
POST /task/add-task
```

**Request Body:**
```json
{
    "title": "Complete Project Report",
    "type": "academic",
    "subject": "Computer Science",
    "priority": "high",
    "deadline": "2024-04-30T23:59:59",
    "estimated_hours": 5.5
}
```

**Response:**
```json
{
    "id": 1,
    "title": "Complete Project Report",
    "type": "academic",
    "subject": "Computer Science",
    "priority": "high",
    "deadline": "2024-04-30T23:59:59",
    "estimated_hours": 5.5,
    "created_at": "2024-04-15T10:00:00",
    "started_at": null,
    "completed_at": null
}
```

### Get Task
```http
GET /task/get-task/{task_id}
```

**Response:**
```json
{
    "id": 1,
    "title": "Complete Project Report",
    "type": "academic",
    "subject": "Computer Science",
    "priority": "high",
    "deadline": "2024-04-30T23:59:59",
    "estimated_hours": 5.5,
    "created_at": "2024-04-15T10:00:00",
    "started_at": null,
    "completed_at": null
}
```

### Update Task
```http
PUT /task/update-task/{task_id}
```

**Request Body:**
```json
{
    "title": "Updated Project Report",
    "priority": "medium",
    "estimated_hours": 6.0
}
```

### Delete Task
```http
DELETE /task/delete-task/{task_id}
```

**Response:**
```json
{
    "message": "Task deleted successfully"
}
```

### Get All Tasks
```http
GET /task/get-tasks
```

### Filter Tasks
```http
GET /task/tasks-by-status/{status}
GET /task/tasks-by-type/{task_type}
GET /task/tasks-by-goal/{goal_id}
```

## Goal Management

### Create Goal
```http
POST /goal/add-goal
```

**Request Body:**
```json
{
    "name": "Complete Semester Projects",
    "type": "academic",
    "target_date": "2024-05-15T23:59:59",
    "target_tasks": ["Project Report", "Final Presentation"]
}
```

### Get Goal
```http
GET /goal/get_goal/{goal_id}
```

### Update Goal
```http
PUT /goal/update-goal/{goal_id}
```

### Delete Goal
```http
DELETE /goal/delete-goal/{goal_id}
```

### Get All Goals
```http
GET /goal/get-goals
```

## Subtask Management

### Create Subtask
```http
POST /subtask/subtasks/
```

**Request Body:**
```json
{
    "title": "Research Phase",
    "estimated_hours": 2.5,
    "task_id": 1
}
```

### Get Subtask
```http
GET /subtask/subtasks/{subtask_id}
```

### Update Subtask
```http
PUT /subtask/subtasks/{subtask_id}
```

### Delete Subtask
```http
DELETE /subtask/subtasks/{subtask_id}
```

## Analysis & Insights

### Task Statistics
```http
GET /analysis/task-statistics/{user_id}
```

**Response:**
```json
{
    "total_tasks": 25,
    "completed_tasks": 15,
    "pending_tasks": 10,
    "tasks_by_type": {
        "academic": 15,
        "personal": 10
    },
    "tasks_by_subject": {
        "Computer Science": 10,
        "Mathematics": 5
    },
    "average_estimated_hours": 4.5,
    "total_estimated_hours": 112.5
}
```

### Goal Progress
```http
GET /analysis/goal-progress/{user_id}
```

### Screen Usage Analysis
```http
GET /analysis/screen-usage/{user_id}?days=7
```

### Performance Metrics
```http
GET /analysis/performance/{user_id}?days=30
```

### Task Completion Trends
```http
GET /analysis/task-trends/{user_id}?days=30
```

### ML-Based Insights

#### Task Completion Prediction
```http
GET /analysis/predict-task-completion-time/{user_id}
```

**Response:**
```json
{
    "model_accuracy": 0.85,
    "feature_importance": {
        "type": 0.25,
        "subject": 0.20,
        "estimated_hours": 0.30,
        "deadline_hours": 0.15,
        "subtask_count": 0.05,
        "high_priority": 0.05
    }
}
```

#### Performance Trend Prediction
```http
GET /analysis/predict-performance-trend/{user_id}
```

#### Screen Usage Pattern Analysis
```http
GET /analysis/analyze-screen-usage-patterns/{user_id}
```

#### Comprehensive ML Insights
```http
GET /analysis/ml-insights/{user_id}
```

## Onboarding

### User Onboarding
```http
POST /onboarding/onboard
```

**Request:**
- `token`: Firebase authentication token
- `audios`: List of audio files (optional)
- `images`: List of image files (required)

**Response:**
```json
{
    "tasks": [...],
    "goals": [...]
}
```

## Error Responses

All endpoints may return the following error responses:

```json
{
    "detail": "User not found"
}
```
Status Code: 404

```json
{
    "detail": "Task not found"
}
```
Status Code: 404

```json
{
    "detail": "Failed to add task"
}
```
Status Code: 400

```json
{
    "detail": "Internal server error"
}
```
Status Code: 500

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- 100 requests per minute per user
- 1000 requests per hour per user

## Best Practices

1. Always include the Firebase token in requests
2. Handle rate limiting by implementing exponential backoff
3. Cache responses when appropriate
4. Use appropriate HTTP methods for each operation
5. Include error handling in your implementation

## Data Models

### Task
```json
{
    "id": "integer",
    "title": "string",
    "type": "string",
    "subject": "string",
    "priority": "string",
    "deadline": "datetime",
    "estimated_hours": "float",
    "created_at": "datetime",
    "started_at": "datetime",
    "completed_at": "datetime"
}
```

### Goal
```json
{
    "id": "integer",
    "name": "string",
    "type": "string",
    "target_date": "datetime",
    "target_tasks": ["string"]
}
```

### Subtask
```json
{
    "id": "integer",
    "title": "string",
    "estimated_hours": "float",
    "task_id": "integer"
}
``` 