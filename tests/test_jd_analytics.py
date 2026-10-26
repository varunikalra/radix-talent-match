import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.main import app


client = TestClient(app)


def test_lists_available_samples():
    response = client.get("/api/jd-analytics/samples")

    assert response.status_code == 200
    assert {item["id"] for item in response.json()} >= {
        "backend_engineer",
        "ai_platform_engineer",
    }


def test_gets_selected_sample():
    response = client.get("/api/jd-analytics/samples/backend_engineer")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == "backend_engineer"
    assert "REST APIs" in payload["text"]


def test_analyzes_job_description_and_maps_categories():
    response = client.post(
        "/api/jd-analytics/analyze",
        json={
            "text": """
Title: Platform Engineer
Responsibilities:
- Build REST APIs with Python and PostgreSQL.
- Operate Docker workloads on AWS.
Requirements:
- 4 years of experience.
- Bachelor's degree in Computer Science.
- Strong communication and problem solving skills.
"""
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] == "Platform Engineer"
    assert payload["requirements"]["experience"] == ["4 years"]
    assert "Python" in payload["technical_skills"]
    assert "Communication" in payload["soft_skills"]

    categories = {item["code"]: item["skills"] for item in payload["radix_categories"]}
    assert "Python" in categories["COD"]
    assert "AWS" in categories["CLOUD"]
    assert "PostgreSQL" in categories["SQL"]
    assert "Communication" in categories["COMM"]


def test_rejects_empty_input():
    response = client.post("/api/jd-analytics/analyze", json={"text": "   "})

    assert response.status_code == 422


def test_missing_and_unstructured_information_remains_empty():
    response = client.post(
        "/api/jd-analytics/analyze",
        json={"text": "General opportunity for energetic people."},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["title"] is None
    assert payload["company"] is None
    assert payload["requirements"] == {"experience": [], "education": []}
    assert payload["technical_skills"] == []
    assert payload["soft_skills"] == []


def test_missing_sample_returns_not_found():
    response = client.get("/api/jd-analytics/samples/not-a-real-jd")

    assert response.status_code == 404
