### Part Rank Pc building tool

This tool allows for easy pc building while checking compatibility, and ranking price to performance for each part using PassMark GPU data.

## Running Commands

# Old Backend
* FastAPI
* cd src\backend
* pip install -r requirements.txt
* python -m uvicorn main:app --reload

# New Backend Run with poetry
* pip install poetry
* cd src\backend\app
* poetry add  (for adding dependencies)
* poetry install 
* poetry run uvicorn app.main:app --reload


# Frontend
* cd src\frontend
* npm install
* npm run dev

# Alembic
* Alembic revision --autogenerate -m "name"
* Alembic upgrade head