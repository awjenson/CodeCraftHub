# CodeCraftHub - Flask REST API + Learning Dashboard

A beginner-friendly full-stack project built with Flask and vanilla JavaScript that lets you create, read, update, and delete (CRUD) courses. The backend stores data in a JSON file, and a browser-based dashboard provides a complete user interface for managing courses.

---

## 1) Project Overview

CodeCraftHub has two parts:

**Backend** — A Flask REST API that exposes endpoints to create, list, fetch, update, and delete courses. Data is persisted in a local JSON file, making it easy to understand how data can be stored without a database.

**Frontend** — A single-page dashboard (`index.html`) built with vanilla HTML, CSS, and JavaScript that connects to the Flask API and provides a full course management interface.

**Key learning points:**

- How to structure a Flask app for a REST API.
- How to handle HTTP methods: GET, POST, PUT, DELETE.
- How to return JSON responses with appropriate HTTP status codes.
- How to connect a frontend to a backend using `fetch()`.
- How to handle CORS when the frontend and backend run on different origins.
- How to write tests with pytest to verify API behavior.

---

## 2) Features

**Backend API:**
- Create a new course (`POST /api/courses`)
- List all courses (`GET /api/courses`)
- Get a course by ID (`GET /api/courses/{id}`)
- Update a course (`PUT /api/courses/{id}`)
- Delete a course (`DELETE /api/courses/{id}`)
- Course statistics (`GET /api/courses/stats`)
- Simple input validation and error handling
- CORS support via `flask-cors` so the frontend can connect from the browser
- Per-test data isolation using a temporary JSON file during tests

**Frontend Dashboard:**
- Stats bar showing total courses and counts by status
- Form to add new courses with validation
- Table listing all courses with status badges
- Edit modal that pre-fills with existing course data
- Delete confirmation modal
- Toast notifications for success and error feedback
- Loading spinners during API calls
- Responsive layout for mobile and tablet screens

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

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install Flask flask-cors pytest
   ```

4. *(Optional)* Run tests to verify your setup:
   ```bash
   pytest -q
   ```

> **Note:** Tests use a temporary data file so they won't affect your real data.

---

## 4) Running the Application

You need to run **two** things: the Flask backend and a local file server for the frontend.

### Step 1 — Start the Flask backend

Ensure your virtual environment is activated, then:

**macOS/Linux:**
```bash
export FLASK_APP=app.py
flask run
```

**Windows:**
```bash
set FLASK_APP=app.py
flask run
```

The backend will start at **http://127.0.0.1:5000**.

Alternatively, if `app.py` includes a `__main__` block:
```bash
python app.py
```

### Step 2 — Serve the frontend

Open a second terminal tab, activate your virtual environment, and run:

```bash
python -m http.server 5500
```

Then open your browser and go to:
```
http://localhost:5500/index.html
```

> **Important:** Do not open `index.html` by double-clicking it in Finder. Opening it as a `file://` URL causes the browser to block API calls due to CORS security rules. Always use the `http.server` approach above.

> **macOS note:** If you see a `403 Forbidden` from `AirTunes/Server` when running `curl -I http://localhost:5000`, macOS AirPlay Receiver is occupying port 5000. Disable it in **System Settings → General → AirDrop & Handoff → AirPlay Receiver**.

---

## 5) API Endpoints

**Base URL:** `http://localhost:5000`

---

### Get Course Statistics

`GET /api/courses/stats`

**Response:** `200 OK`
```json
{
  "total": 3,
  "by_status": {
    "Not Started": 1,
    "In Progress": 1,
    "Completed": 1
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/courses/stats
```

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
  "status": "Not Started",
  "created_at": "2026-04-28T18:00:00Z"
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
    "status": "Not Started",
    "created_at": "2026-04-28T18:00:00Z"
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
  "status": "Not Started",
  "created_at": "2026-04-28T18:00:00Z"
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
  "status": "In Progress",
  "created_at": "2026-04-28T18:00:00Z"
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
- Flask, flask-cors, and pytest installed

### Steps

1. Activate your virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the tests:
   ```bash
   pytest -q
   ```

### What the tests cover

- Creating, listing, retrieving by ID, updating, and deleting courses
- Course statistics endpoint
- Handling of missing or invalid fields
- Basic error cases (not found, bad requests)

> **Note:** Tests use a temporary data file — your real data won't be affected.

---

## 7) Troubleshooting

**`ModuleNotFoundError: No module named 'app'`**
Ensure you're in the project root and that the app file exists, and that the imports in tests refer to the correct module.

**"Failed to fetch" / CORS error in the browser**
Do not open `index.html` directly from Finder. Serve it with `python -m http.server 5500` and open `http://localhost:5500/index.html` instead.

**Port 5000 returning `403 Forbidden` from AirTunes (macOS)**
macOS AirPlay Receiver uses port 5000. Disable it in **System Settings → General → AirDrop & Handoff → AirPlay Receiver**, then restart Flask.

**Bad requests or 404s**
Verify the route paths and IDs match what the app exposes.

**Data file permissions**
If your app writes to a JSON file, ensure the path is writable, or use a temp path during tests.

**Virtual environment not activating**
Make sure you're using the correct activation command for your OS and that your shell reflects the venv's Python.

**Dependency issues**
```bash
pip install -r requirements.txt
```

---

## 8) Project Structure

```
CodeCraftHub/
├── app.py              # Flask REST API with all endpoints
├── index.html          # Frontend dashboard (HTML/CSS/JavaScript)
├── courses.json        # Local data file (auto-created, not committed)
├── tests/
│   └── test_api.py     # pytest tests for the API
├── .venv/              # Python virtual environment (local, not committed)
├── requirements.txt    # Python dependencies list
└── README.md           # This file
```

**What each part does:**

- **`app.py`** — The main Flask application. Defines all REST API routes, validation helpers, and file storage logic. Also includes CORS support via `flask-cors`.
- **`index.html`** — The frontend dashboard. A single self-contained file with embedded CSS and JavaScript that connects to the Flask API and provides a full CRUD interface.
- **`courses.json`** — The data file where courses are stored. Auto-created on first run. Not committed to Git.
- **`tests/test_api.py`** — Automated tests that exercise all API endpoints to ensure they work as expected.
- **`.venv/`** — A self-contained Python environment so dependencies don't interfere with other projects.
- **`requirements.txt`** — The list of Python packages the project needs. Install with `pip install -r requirements.txt`.
- **`README.md`** — This document, explaining how to use the project.