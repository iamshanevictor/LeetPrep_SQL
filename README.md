# LeetPrep-SQL

LeetPrep-SQL is a Flask and Vue-based SQL practice platform designed to help learners master recurring SQL interview patterns before solving LeetCode-style SQL problems.

The app now includes a JSON-backed roadmap learning system. The roadmap teaches SQL through a tutorial -> guided example -> practice -> boss problem flow, so advanced problems are reached gradually instead of dropped in all at once.

## Current Status

This version includes:

- Flask app factory and REST API structure
- Vue 3 + Vite single-page app
- Roadmap overview with 10 target SQL modules
- Complete roadmap content for Modules 1-10
- Cumulative module metadata showing which earlier modules each module builds on
- DuckDB-backed in-memory query execution for learning content
- Basic grading by comparing user query output with expected query output
- SQL safety checks that only allow `SELECT` and `WITH` learner queries

Each module now includes tutorial lessons, guided examples, practice prompts, and a boss problem backed by DuckDB seed data.

## Tech Stack

- Backend: Flask
- Frontend: Vue 3
- Frontend tooling: Vite
- API style: REST API
- SQL execution for lessons: DuckDB
- Future app database: SQLite
- Future ORM: SQLAlchemy
- Workflow: Python-first, no Docker

## Learning Flow

Each completed roadmap module is designed to follow this path:

1. Concept tutorial
2. Small guided example
3. Slightly harder practice problem
4. Pattern explanation and mental model
5. Final boss problem

The roadmap currently covers:

- `GROUP BY`
- `AVG`
- `INNER JOIN`
- `CASE WHEN`
- `CTE`
- `MIN` and `MAX`
- Subquery exclusion patterns
- Consecutive row grouping
- `LEFT JOIN` and zero-count buckets
- Date interval grouping
- Conditional aggregation and pivot-style reports
- `DENSE_RANK`
- Moving averages
- Pair generation and distance calculations
- `LAG` and `LEAD`

## Folder Structure

```text
backend/
  app/
    api/               Flask route blueprints
    services/          Loading, DuckDB execution, and grading services
    models/            Future SQLAlchemy models
    utils/             SQL safety helpers
  learning_content/    Roadmap and lesson JSON files
  problems/            Future standalone SQL problem JSON files
  scripts/             Future maintenance scripts
  tests/               Backend tests
frontend/
  src/
    api/               Frontend API client helpers
    components/        Reusable Vue components
    pages/             Route-level Vue pages
    router/            Vue Router setup
```

## Run the Backend

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

The Flask API runs at:

```text
http://localhost:5000
```

## Run the Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The Vue app runs at:

```text
http://localhost:5173
```

Copy `frontend/.env.example` to `frontend/.env` if you want to customize the API base URL.

## Open the Roadmap

With both servers running, open:

```text
http://localhost:5173/roadmap
```

Module 1 is available at:

```text
http://localhost:5173/roadmap/module_01_salary_comparison
```

## API Endpoints

Core endpoints:

```text
GET  /api/health
GET  /api/problems
GET  /api/problems/<problem_id>
POST /api/problems/<problem_id>/run
POST /api/problems/<problem_id>/submit
GET  /api/attempts
```

Roadmap endpoints:

```text
GET  /api/roadmap
GET  /api/modules
GET  /api/modules/<module_id>
GET  /api/modules/<module_id>/lessons/<lesson_id>
POST /api/modules/<module_id>/lessons/<lesson_id>/run
POST /api/modules/<module_id>/lessons/<lesson_id>/submit
GET  /api/modules/<module_id>/boss
POST /api/modules/<module_id>/boss/run
POST /api/modules/<module_id>/boss/submit
```

## Test Module 1 Lesson 1

Run this after starting the backend:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:5000/api/modules/module_01_salary_comparison/lessons/lesson_01_group_by_avg/submit `
  -ContentType "application/json" `
  -Body '{"query":"SELECT department_id, SUM(salary) AS total_salary FROM employees GROUP BY department_id"}'
```

## Test the Module 1 Boss Problem

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://localhost:5000/api/modules/module_01_salary_comparison/boss/submit `
  -ContentType "application/json" `
  -Body '{"query":"WITH department_averages AS (SELECT d.department_name, AVG(e.salary) AS department_avg_salary FROM employees e INNER JOIN departments d ON e.department_id = d.department_id GROUP BY d.department_name), company_average AS (SELECT AVG(salary) AS company_avg_salary FROM employees) SELECT da.department_name, da.department_avg_salary, ca.company_avg_salary, CASE WHEN da.department_avg_salary > ca.company_avg_salary THEN ''higher'' WHEN da.department_avg_salary < ca.company_avg_salary THEN ''lower'' ELSE ''same'' END AS comparison_result FROM department_averages da CROSS JOIN company_average ca"}'
```

## Run Backend Tests

From the `backend` directory:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Where Learning Content Lives

Roadmap metadata:

```text
backend/learning_content/roadmap.json
```

Module lesson and boss content:

```text
backend/learning_content/modules/
```

Each module folder contains lesson JSON files and a `boss_problem.json` file. For example:

```text
backend/learning_content/modules/module_02_quiet_students/
```

When revising or adding content, keep `lessons_count` and `builds_on_modules` in `backend/learning_content/roadmap.json` in sync with the authored lesson files.

## What Is Intentionally Not Implemented Yet

- Standalone practice problems under `backend/problems/`
- User progress persistence
- Daily practice tracking
- Authentication or login
- Database migrations
- CodeMirror or advanced SQL editor integration
- Docker
- Production static serving from Flask

## Files to Study First

- `backend/app/services/learning_loader.py` for JSON roadmap loading
- `backend/app/services/sql_runner.py` for DuckDB execution
- `backend/app/services/grader.py` for result comparison
- `backend/app/api/learning.py` for thin roadmap API routes
- `backend/learning_content/roadmap.json` for module metadata
- `frontend/src/pages/RoadmapPage.vue` for the roadmap UI
- `frontend/src/pages/LessonPage.vue` for the lesson workbench
- `frontend/src/api/roadmap.js` for frontend/backend learning API calls

## Next Planned Features

- Add richer sample explanations and alternative solutions for each module
- Persist lesson and boss problem attempts in SQLite
- Track daily practice and streaks
- Add standalone problem loading under `backend/problems/`
- Add richer SQL editor support later
