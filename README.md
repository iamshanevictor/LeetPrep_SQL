# LeetPrep-SQL

LeetPrep-SQL is a Flask and Vue-based SQL practice platform designed to help learners master recurring SQL interview patterns before solving LeetCode-style SQL problems. This initial version focuses on building the project foundation, API structure, frontend layout, and reusable service placeholders before adding real practice problems.

## Current Status

This repository is scaffold-only. It can run successfully without practice problems, but it intentionally does not include problem JSON files, DuckDB execution, grading, authentication, migrations, Docker, or a production build pipeline.

## Tech Stack

- Backend: Flask
- Frontend: Vue 3
- Frontend tooling: Vite
- API style: REST API
- Future SQL execution engine: DuckDB
- Future app database: SQLite
- Future ORM: SQLAlchemy
- Workflow: Python-first, no Docker

## Folder Structure

```text
backend/
  app/
    api/          Flask route blueprints
    services/     Placeholder business logic services
    models/       Future SQLAlchemy models
    utils/        Shared backend utilities
  problems/       Future SQL problem JSON files
  scripts/        Future maintenance scripts
  tests/          Backend tests
frontend/
  src/
    api/          Frontend API client helpers
    components/   Reusable Vue components
    pages/        Route-level Vue pages
    router/       Vue Router setup
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

## Available API Endpoints

```text
GET  /api/health
GET  /api/problems
GET  /api/problems/<problem_id>
POST /api/problems/<problem_id>/run
POST /api/problems/<problem_id>/submit
GET  /api/attempts
```

Current endpoint behavior:

- `GET /api/health` returns the app health status.
- `GET /api/problems` returns an empty problem list.
- `GET /api/problems/<problem_id>` returns a 404 placeholder response.
- `POST /api/problems/<problem_id>/run` returns a 501 placeholder response.
- `POST /api/problems/<problem_id>/submit` returns a 501 placeholder response.
- `GET /api/attempts` returns an empty attempts list.

## Test the Health Endpoint

With the backend running:

```powershell
Invoke-RestMethod http://localhost:5000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "app": "LeetPrep-SQL"
}
```

## Run Backend Tests

From the `backend` directory:

```powershell
pytest
```

## What Is Intentionally Not Implemented Yet

- Practice SQL problems
- Starter SQL question JSON files
- Real DuckDB query execution
- Real grading
- Problem generation
- Daily practice tracking
- Authentication or login
- Database migrations
- CodeMirror or advanced SQL editor integration
- Docker
- Production static serving from Flask

## Where Future SQL Problems Will Go

Add future problem JSON files under:

```text
backend/problems/easy/
backend/problems/medium/
backend/problems/hard/
```

Reusable generation templates can later go under:

```text
backend/problems/templates/
```

## Files to Study First

- `backend/app/__init__.py` for the Flask app factory pattern
- `backend/app/api/problems.py` for thin REST route structure
- `backend/app/services/problem_loader.py` for where problem loading will grow
- `backend/app/utils/sql_safety.py` for the first reusable backend utility
- `frontend/src/api/client.js` for frontend/backend communication
- `frontend/src/router/index.js` for Vue route setup
- `frontend/src/pages/ProblemListPage.vue` for API fetching in Vue

## Next Planned Features

- Define the SQL problem JSON format
- Load problem files from `backend/problems/`
- Add DuckDB-backed query execution
- Add result comparison and grading
- Store attempts in SQLite with SQLAlchemy
- Add daily practice and streak tracking
- Add problem generation from templates
