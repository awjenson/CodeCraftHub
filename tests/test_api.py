# tests/test_api.py
import json
import os
import tempfile
import sys
import pathlib

import pytest

# Ensure the project root is on sys.path so Python can import app
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

# Import the Flask app and the module that defines DATA_FILE
from app import app as flask_app
import app as app_module  # to override DATA_FILE in tests

@pytest.fixture
def client():
    # Create a fresh temp directory for each test function
    with tempfile.TemporaryDirectory() as tmpdir:
        app_module.DATA_FILE = os.path.join(tmpdir, "courses.json")
        # Initialize with an empty list
        with open(app_module.DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        with flask_app.test_client() as client:
            yield client

def test_create_course(client):
    payload = {
        "name": "Python Basics",
        "description": "Intro to Python",
        "target_date": "2026-12-01",
        "status": "Not Started"
    }
    resp = client.post("/api/courses", json=payload)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "id" in data
    assert data["name"] == payload["name"]

def test_get_all_courses(client):
    resp = client.get("/api/courses")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

def test_get_course_by_id(client):
    # Create a course first
    payload = {
        "name": "Module Test",
        "description": "Testing fetch by id",
        "target_date": "2026-12-01",
        "status": "Not Started"
    }
    post_resp = client.post("/api/courses", json=payload)
    cid = post_resp.get_json()["id"]

    resp = client.get(f"/api/courses/{cid}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == cid

def test_update_course(client):
    payload = {
        "name": "Update Test",
        "description": "Before update",
        "target_date": "2026-11-01",
        "status": "Not Started"
    }
    post_resp = client.post("/api/courses", json=payload)
    cid = post_resp.get_json()["id"]

    update = {
        "name": "Update Test",
        "description": "After update",
        "target_date": "2027-01-15",
        "status": "In Progress"
    }
    resp = client.put(f"/api/courses/{cid}", json=update)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["name"] == update["name"]
    assert data["target_date"] == update["target_date"]
    assert data["status"] == update["status"]

def test_delete_course(client):
    payload = {
        "name": "Delete Me",
        "description": "Temp record",
        "target_date": "2026-12-01",
        "status": "Not Started"
    }
    post_resp = client.post("/api/courses", json=payload)
    cid = post_resp.get_json()["id"]

    resp = client.delete(f"/api/courses/{cid}")
    assert resp.status_code == 200
    assert resp.get_json().get("message") == "Course deleted"

def test_get_not_found(client):
    resp = client.get("/api/courses/99999")
    assert resp.status_code == 404

def test_post_missing_field(client):
    payload = {
        "description": "No name",
        "target_date": "2026-12-01",
        "status": "Not Started"
    }
    resp = client.post("/api/courses", json=payload)
    assert resp.status_code == 400

def test_post_invalid_date(client):
    payload = {
        "name": "BadDate",
        "description": "Wrong date format",
        "target_date": "2026/12/01",
        "status": "Not Started"
    }
    resp = client.post("/api/courses", json=payload)
    assert resp.status_code == 400

def test_post_invalid_status(client):
    payload = {
        "name": "BadStatus",
        "description": "Invalid status",
        "target_date": "2026-12-01",
        "status": "Done"
    }
    resp = client.post("/api/courses", json=payload)
    assert resp.status_code == 400

def test_post_no_json_body(client):
    resp = client.post("/api/courses", data="", content_type="application/json")
    assert resp.status_code == 400

def test_get_stats(client):
    # Create courses with different statuses
    client.post("/api/courses", json={
        "name": "Course 1",
        "description": "Desc",
        "target_date": "2026-12-01",
        "status": "Not Started"
    })
    client.post("/api/courses", json={
        "name": "Course 2",
        "description": "Desc",
        "target_date": "2026-12-01",
        "status": "In Progress"
    })

    resp = client.get("/api/courses/stats")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] == 2
    assert data["by_status"]["Not Started"] == 1
    assert data["by_status"]["In Progress"] == 1
    assert data["by_status"]["Completed"] == 0