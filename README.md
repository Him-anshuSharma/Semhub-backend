# SemHub Backend

SemHub is a comprehensive task and goal management system with advanced analytics and machine learning capabilities.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Environment Configuration](#environment-configuration)
5. [API Documentation](#api-documentation)
6. [Database Schema](#database-schema)
7. [Machine Learning Features](#machine-learning-features)
8. [Development Guidelines](#development-guidelines)
9. [Deployment](#deployment)

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Firebase Account
- Redis (for caching)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/semhub-backend.git
cd semhub-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize the database
python scripts/init_db.py

# Run the application
uvicorn app.main:app --reload
```

## Project Structure
```
semhub-backend/
├── app/
│   ├── main.py
│   ├── routers/
│   │   ├── task_routes.py
│   │   ├── goal_routes.py
│   │   ├── subtask_routes.py
│   │   ├── analysis_routes.py
│   │   └── onboarding_routes.py
│   ├── models/
│   │   ├── pydantic_models.py
│   │   └── sqlalchemy_models.py
│   └── services/
│       ├── analysis_services.py
│       ├── task_services.py
│       └── goal_services.py
├── db/
│   ├── models/
│   │   └── sqlalchemy_models.py
│   └── services/
│       ├── db_services.py
│       └── user_services.py
├── tests/
├── scripts/
├── .env.example
├── requirements.txt
└── README.md
```

## Setup and Installation

### 1. Environment Setup
Create a `.env` file with the following variables:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/semhub
FIREBASE_CREDENTIALS_PATH=path/to/firebase-credentials.json
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
```

### 2. Database Setup
```bash
# Create database
createdb semhub

# Run migrations
alembic upgrade head
```

### 3. Firebase Setup
1. Create a Firebase project
2. Download service account credentials
3. Place credentials file in secure location
4. Update `.env` with credentials path

## Environment Configuration

### Development
```bash
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=DEBUG
```

### Production
```bash
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
```

## API Documentation

### Authentication
All API endpoints require Firebase authentication. Include the Firebase token in the request header:
```http
Authorization: Bearer <firebase_token>
```

### Key Endpoints

#### Task Management
```http
POST /task/add-task
GET /task/get-task/{task_id}
PUT /task/update-task/{task_id}
DELETE /task/delete-task/{task_id}
GET /task/get-tasks
```

#### Goal Management
```http
POST /goal/add-goal
GET /goal/get_goal/{goal_id}
PUT /goal/update-goal/{goal_id}
DELETE /goal/delete-goal/{goal_id}
GET /goal/get-goals
```

#### Analysis
```http
GET /analysis/task-statistics/{user_id}
GET /analysis/goal-progress/{user_id}
GET /analysis/screen-usage/{user_id}
GET /analysis/performance/{user_id}
GET /analysis/ml-insights/{user_id}
```

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## Database Schema

### Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    firebase_uid VARCHAR(255) UNIQUE NOT NULL
);
```

### Tasks
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    subject VARCHAR(50) NOT NULL,
    priority VARCHAR(10),
    deadline TIMESTAMP,
    estimated_hours NUMERIC(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    user_id INTEGER REFERENCES users(id)
);
```

### Goals
```sql
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    target_date TIMESTAMP,
    user_id INTEGER REFERENCES users(id)
);
```

## Machine Learning Features

### Task Completion Prediction
- Uses Random Forest Regression
- Features: task type, subject, estimated hours, deadline, subtasks
- Predicts completion time for new tasks

### Performance Analysis
- Time-series analysis of user performance
- Predicts future performance trends
- Identifies optimal working patterns

### Screen Usage Analysis
- Pattern recognition in app usage
- Optimal usage time recommendations
- Productivity impact analysis

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Keep functions small and focused

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Git Workflow
1. Create feature branch
2. Write tests
3. Implement feature
4. Run tests
5. Create pull request

## Deployment

### Docker Deployment
```bash
# Build image
docker build -t semhub-backend .

# Run container
docker run -p 8000:8000 semhub-backend
```

### Production Considerations
1. Use production-grade server (e.g., Gunicorn)
2. Set up proper logging
3. Configure rate limiting
4. Enable caching
5. Set up monitoring

### Monitoring
- Use Prometheus for metrics
- Grafana for visualization
- Sentry for error tracking

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License
MIT License - see LICENSE file for details 