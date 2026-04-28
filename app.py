"""
CodeCraftHub - Lightweight Flask REST API for tracking learning courses.

High-level summary (what this file does):
- Exposes a CRUD REST API for "courses" under /api/courses and /api/courses/<id>.
- Stores data in a JSON file named courses.json at the project root (auto-created if missing).
- Each course has:
    - id: auto-generated starting from 1
    - name: required
    - description: required
    - target_date: required, format YYYY-MM-DD
    - status: required, one of ["Not Started", "In Progress", "Completed"]
    - created_at: auto-generated timestamp (UTC)
- Supports:
    - POST /api/courses to create
    - GET /api/courses to fetch all
    - GET /api/courses/<id> to fetch a single
    - PUT /api/courses/<id> to update
    - DELETE /api/courses/<id> to delete
- Includes thorough error handling for:
    - Missing/invalid fields
    - Course not found
    - Invalid status values
    - File read/write errors
- Includes helpful comments for beginners and a future-refactor note to move API code into an api/ folder later.
- Uses a simple file-level lock to help with concurrent access in the dev server.

Notes:
- This is designed for learning REST basics. For production, consider a real DB and proper error logging.
"""

from flask import Flask, request, jsonify
import json
import os
import threading
from datetime import datetime, timezone
from flask_cors import CORS

# ----------------------------
# Future refactor note for your future self
# ----------------------------
# You asked to move API-related code into an api/ folder in the future.
# This is a gentle reminder and a plan to help you refactor without breaking
# current functionality.

# Plan (when you're ready to refactor):
# 1) Create an api/ package with an __init__.py that defines a Flask Blueprint named 'api'.
#    - api/__init__.py:
#        from flask import Blueprint
#        api = Blueprint('api', __name__)
#        from . import courses  # register routes inside the blueprint
# 2) Move all route handlers (POST /api/courses, GET /api/courses, etc.) into api/courses.py
# 3) Move shared storage/validation helpers into api/storage.py
#    - api/storage.py would contain:
#        - load_courses()
#        - save_courses()
#        - next_id()
#        - find_course()
#        - current_timestamp()
#        - valid_date()
#        - validate_course_payload()
# 4) In app.py, create the Flask app and register the blueprint:
#        from api import api as api_blueprint
#        app.register_blueprint(api_blueprint, url_prefix='/api')
# 5) Update the DATA_FILE path to a subdirectory like data/courses.json and ensure the
#    folder is created if it doesn't exist.
# 6) Update error handling as needed for the new module boundaries.
# 7) Optional: add unit tests under tests/ for the blueprint endpoints.
# 
# This single-file implementation is great for learning. When you're ready to scale,
# follow this plan to improve organization and testability.

# ----------------------------
# Configuration and constants
# ----------------------------
# Path to the JSON file that will store all courses
DATA_FILE = 'courses.json'

# Allowed status values
STATUS_OPTIONS = ["Not Started", "In Progress", "Completed"]

# A simple in-process lock to make file read/write a bit safer in the dev server
_FILE_LOCK = threading.Lock()

# ----------------------------
# Helper functions
# ----------------------------

def load_courses():
    """
    Load and return the list of courses from the JSON file.
    If the file doesn't exist, return an empty list.
    If the file is corrupted/empty, also return an empty list.
    Any file I/O errors should be handled by the caller.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with _FILE_LOCK:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
    except (OSError, json.JSONDecodeError) as e:
        # Re-raise as a general exception for the caller to convert into a 500 error
        raise

def save_courses(courses):
    """
    Save the list of courses to the JSON file.
    Creates the file if it doesn't exist.
    """
    try:
        with _FILE_LOCK:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(courses, f, indent=2, ensure_ascii=False)
    except OSError as e:
        # Propagate the error to be handled by the caller
        raise

def next_id(courses):
    """
    Compute the next auto-incremented ID for a new course.
    Starts at 1 if the list is empty.
    """
    if not courses:
        return 1
    return max((c.get('id', 0) for c in courses), default=0) + 1

def find_course(courses, course_id):
    """
    Find and return a course by its ID, or None if not found.
    """
    for course in courses:
        if course.get('id') == course_id:
            return course
    return None

def current_timestamp():
    """
    Return a UTC timestamp string for created_at.
    Format: YYYY-MM-DDTHH:MM:SSZ
    """
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def valid_date(date_str):
    """
    Validate that date_str is in YYYY-MM-DD format.
    Returns True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False

def validate_course_payload(data, require_all=True):
    """
    Validate the incoming payload for creating/updating a course.

    - name: required, non-empty string
    - description: required, non-empty string
    - target_date: required, format YYYY-MM-DD
    - status: required, one of STATUS_OPTIONS
    - When require_all is False, this function can be used for partial validation.
    Returns (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Invalid payload: expected a JSON object"

    name = data.get('name')
    description = data.get('description')
    target_date = data.get('target_date')
    status = data.get('status')

    # Basic required field checks
    if require_all:
        if not name or not isinstance(name, str) or not name.strip():
            return False, "Missing or invalid required field: name"
        if not description or not isinstance(description, str) or not description.strip():
            return False, "Missing or invalid required field: description"
        if not target_date or not isinstance(target_date, str) or not target_date.strip():
            return False, "Missing or invalid required field: target_date"
        if not valid_date(target_date):
            return False, "target_date must be in YYYY-MM-DD format"
        if not status or not isinstance(status, str) or status not in STATUS_OPTIONS:
            return False, f"status must be one of {STATUS_OPTIONS}"
    else:
        # Partial validation (used for PUT/PATCH if desired)
        if name is not None and (not isinstance(name, str) or not name.strip()):
            return False, "Invalid field: name"
        if description is not None and (not isinstance(description, str) or not description.strip()):
            return False, "Invalid field: description"
        if target_date is not None:
            if not isinstance(target_date, str) or not valid_date(target_date):
                return False, "Invalid field: target_date must be YYYY-MM-DD"
        if status is not None:
            if not isinstance(status, str) or status not in STATUS_OPTIONS:
                return False, f"status must be one of {STATUS_OPTIONS}"

    return True, ""

# ----------------------------
# Flask app and routes
# ----------------------------
app = Flask(__name__)

# ── CORS (Cross-Origin Resource Sharing) ────────────────────────────────────
# When the frontend (index.html) runs in a browser and makes fetch() calls to
# the Flask backend, the browser blocks those requests by default if the two
# are on different "origins" (e.g. file:// vs http://localhost:5000).
# flask-cors adds the necessary HTTP headers to Flask's responses to tell the
# browser it's safe to allow those cross-origin requests.
CORS(app)

@app.route('/api/courses', methods=['POST'])
def add_course():
    """
    Create a new course.
    Expects JSON body with: name, description, target_date, status
    Automatically assigns id and created_at.
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    is_valid, err = validate_course_payload(payload, require_all=True)
    if not is_valid:
        return jsonify({"error": err}), 400

    try:
        courses = load_courses()
        course_id = next_id(courses)
        new_course = {
            "id": course_id,
            "name": payload["name"],
            "description": payload["description"],
            "target_date": payload["target_date"],
            "status": payload["status"],
            "created_at": current_timestamp()
        }
        courses.append(new_course)
        save_courses(courses)
        return jsonify(new_course), 201
    except OSError as e:
        # File IO error
        return jsonify({"error": "Failed to read/write data file"}), 500
    except Exception as e:
        # Catch-all for unexpected errors
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    """
    Retrieve all courses.
    """
    try:
        courses = load_courses()
        return jsonify(courses), 200
    except OSError:
        return jsonify({"error": "Failed to read data file"}), 500
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    """
    Retrieve a single course by its ID.
    """
    try:
        courses = load_courses()
        course = find_course(courses, course_id)
        if course is None:
            return jsonify({"error": "Course not found"}), 404
        return jsonify(course), 200
    except OSError:
        return jsonify({"error": "Failed to read data file"}), 500
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    Update an existing course by ID.
    Expects full payload: name, description, target_date, status
    The id and created_at fields are preserved.
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    is_valid, err = validate_course_payload(payload, require_all=True)
    if not is_valid:
        return jsonify({"error": err}), 400

    try:
        courses = load_courses()
        course = find_course(courses, course_id)
        if course is None:
            return jsonify({"error": "Course not found"}), 404

        # Update allowed fields; preserve id and created_at
        course.update({
            "name": payload["name"],
            "description": payload["description"],
            "target_date": payload["target_date"],
            "status": payload["status"]
            # created_at and id remain unchanged
        })
        save_courses(courses)
        return jsonify(course), 200
    except OSError:
        return jsonify({"error": "Failed to write data file"}), 500
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/courses/stats', methods=['GET'])
def get_stats():
    """
    Return statistics about all courses.
    - total: total number of courses
    - by_status: count of courses for each status option
    """
    try:
        courses = load_courses()
        by_status = {status: 0 for status in STATUS_OPTIONS}
        for course in courses:
            status = course.get('status')
            if status in by_status:
                by_status[status] += 1
        return jsonify({
            "total": len(courses),
            "by_status": by_status
        }), 200
    except OSError:
        return jsonify({"error": "Failed to read data file"}), 500
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Delete a course by ID.
    """
    try:
        courses = load_courses()
        course = find_course(courses, course_id)
        if course is None:
            return jsonify({"error": "Course not found"}), 404

        courses = [c for c in courses if c.get('id') != course_id]
        save_courses(courses)
        return jsonify({"message": "Course deleted"}), 200
    except OSError:
        return jsonify({"error": "Failed to write data file"}), 500
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

# ----------------------------
# Run the app
# ----------------------------
if __name__ == '__main__':
    # Ensure the JSON file exists (empty array) so the app is ready to go on first run
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2, ensure_ascii=False)
        except OSError:
            # If we fail to create the file for any reason, we still run the app.
            # The first request will fail with a 500 indicating the read/write issue.
            pass

    app.run(debug=True)