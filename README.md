# CodeCraftHub - Flask REST API for Courses
 
A beginner-friendly REST API built with Flask that lets you create, read, update, and delete (CRUD) courses. Data is stored in a JSON file, and tests are provided to ensure the API behaves as expected.
 
---
 
## 1) Project Overview
 
CodeCraftHub is a small Flask application that demonstrates how to build a simple REST API for managing courses. It exposes endpoints to create new courses, list all courses, fetch a course by ID, update a course, and delete a course. The API uses a JSON file to persist data, which makes it easy to understand how data can be stored without a database.
 
**Key learning points:**
 
- How to structure a Flask app for a REST API.
- How to handle HTTP methods: GET, POST, PUT, DELETE.
- How to return JSON responses with appropriate HTTP status codes.
- How to write tests with pytest to verify API behavior.
---
 
## 2) Features
 
- Create a new course (`POST /api/courses`)
- List all courses (`GET /api/courses`)
- Get a course by ID (`GET /api/courses/{id}`)
- Update a course (`PUT /api/courses/{id}`)
- Delete a course (`DELETE /api/courses/{id}`)
- Simple input validation and error handling
- Per-test data isolation using a temporary JSON file during tests
---
 
## 3) Installation
 
### Prerequisites
 
- Python 3.8 or newer
- Internet connection to install dependencies
### Steps
 
1. Create a project directory (if you haven't already) and navigate into it.
2. Create a virtual environment (recommended):
   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
 
   **Windows:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
 
3. Install dependencies. If you have a `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   Otherwise, install Flask and pytest manually:
   ```bash
   pip install Flask pytest
   ```
 
4. *(Optional)* Create a `requirements.txt` for sharing:
   ```
   Flask>=2.0
   pytest>=7.0
   ```
 
5. *(Optional)* Run tests to verify your setup:
   ```bash
   pytest -q
   ```
 
> **Note:** Tests use a temporary data file so they won't affect your real data.
 
---
 
## 4) Running the Application
 
### Option A: Flask CLI *(recommended)*
 
1. Ensure your virtual environment is activated.
2. Set the Flask app environment variable:
   **macOS/Linux:**
   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development  # optional, enables debug mode
   ```
 
   **Windows:**
   ```bash
   set FLASK_APP=app.py
   set FLASK_ENV=development
   ```
 
3. Start the server:
   ```bash
   flask run
   ```
 
### Option B: Run directly
 
If `app.py` includes a `__main__` block:
```bash
python app.py
```
 
The server will start at **http://127.0.0.1:5000**. You can test endpoints using `curl`, [Postman](https://www.postman.com/), or [Insomnia](https://insomnia.rest/).
 
> **Note:** The API serves endpoints under `/api/courses`. Data is stored in a JSON file (e.g., `courses.json` by default). You can modify the path in the app code if needed.
 
---
 
## 5) API Endpoints
 
**Base URL:** `http://localhost:5000`
 
---
 
### Create a Course
 
`POST /api/courses`
 
**Request body:**
```json
{
  "name": "Python Basics",
  "description": "Intro to Python",
  "target_date": "2026-12-01",
  "status": "Not Started"
}
```
 
**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Python Basics",
  "description": "Intro to Python",
  "target_date": "2026-12-01",
  "status": "Not Started"
}
```
 
**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"Python Basics","description":"Intro to Python","target_date":"2026-12-01","status":"Not Started"}' \
     http://localhost:5000/api/courses
```
 
---
 
### List All Courses
 
`GET /api/courses`
 
**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Python Basics",
    "description": "Intro to Python",
    "target_date": "2026-12-01",
    "status": "Not Started"
  }
]
```
 
**Example:**
```bash
curl -s http://localhost:5000/api/courses | jq
```
 
---
 
### Get a Course by ID
 
`GET /api/courses/{id}`
 
**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Python Basics",
  "description": "Intro to Python",
  "target_date": "2026-12-01",
  "status": "Not Started"
}
```
 
**Example:**
```bash
curl http://localhost:5000/api/courses/1
```
 
---
 
### Update a Course
 
`PUT /api/courses/{id}`
 
**Request body:**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "target_date": "2027-01-15",
  "status": "In Progress"
}
```
 
**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Updated Name",
  "description": "Updated description",
  "target_date": "2027-01-15",
  "status": "In Progress"
}
```
 
**Example:**
```bash
curl -X PUT -H "Content-Type: application/json" \
     -d '{"name":"Updated Name","description":"Updated description","target_date":"2027-01-15","status":"In Progress"}' \
     http://localhost:5000/api/courses/1
```
 
---
 
### Delete a Course
 
`DELETE /api/courses/{id}`
 
**Response:** `200 OK`
```json
{
  "message": "Course deleted"
}
```
 
**Example:**
```bash
curl -X DELETE http://localhost:5000/api/courses/1
```
 
---
 
### Common Error Responses
 
| Status | Meaning | Example |
|--------|---------|---------|
| `400 Bad Request` | Missing required fields or invalid payload | `POST /api/courses` with missing `"name"` |
| `404 Not Found` | No course with the given ID | `GET /api/courses/99999` |
| `500 Internal Server Error` | Unexpected server issue | Not expected in normal use |
 
---
 
## 6) Testing
 
### Prerequisites
 
- Python and a virtual environment (recommended)
- Flask and pytest installed
### Steps
 
1. Activate your virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install Flask pytest
   ```
3. Run the tests:
   ```bash
   pytest -q
   ```
 
### What the tests cover
 
- Creating, listing, retrieving by ID, updating, and deleting courses
- Handling of missing or invalid fields
- Basic error cases (not found, bad requests)
> **Note:** Tests use a temporary data file — your real data won't be affected.
 
---
 
## 7) Troubleshooting
 
**`ModuleNotFoundError: No module named 'app'`**
Ensure you're in the project root and that the app file exists, and that the imports in tests refer to the correct module.
 
**Bad requests or 404s**
Verify the route paths and IDs in the README match what the app exposes.
 
**Data file permissions**
If your app writes to a JSON file, ensure the path is writable, or use a temp path during tests.
 
**Virtual environment not activating**
Make sure you're using the correct activation command for your OS and that your shell reflects the venv's Python.
 
**Dependency issues**
```bash
pip install -r requirements.txt
```
Or install Flask and pytest manually as shown in the installation steps.
 
---
 
## 8) Project Structure
 
```
CodeCraftHub/
├── app.py              # Flask application with REST API endpoints
├── tests/
│   └── test_api.py     # pytest tests for the API
├── .venv/              # Python virtual environment (local, not committed)
├── requirements.txt    # (Optional) dependencies list
└── README.md           # This file
```
 
**What each part does:**
 
- **`app.py`** — The main application file where the Flask app is created and routes (endpoints) are defined.
- **`tests/test_api.py`** — Automated tests that exercise the API endpoints to ensure they work as expected.
- **`.venv/`** — A self-contained Python environment so dependencies don't interfere with other projects.
- **`requirements.txt`** — A list of Python packages your project needs (Flask, pytest, etc.). Makes installing dependencies easy with `pip install -r requirements.txt`.
- **`README.md`** — This document, explaining how to use the project.