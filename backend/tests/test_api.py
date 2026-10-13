from fastapi.testclient import TestClient

from app.main import app


def test_health_reports_ok():
    with TestClient(app) as client:
        r = client.get("/api/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


def test_create_then_list_note():
    with TestClient(app) as client:
        created = client.post("/api/notes", json={"text": "hello azure"})
        assert created.status_code == 201
        note_id = created.json()["id"]

        listed = client.get("/api/notes")
        assert listed.status_code == 200
        assert note_id in [n["id"] for n in listed.json()]


def test_rejects_empty_note():
    with TestClient(app) as client:
        r = client.post("/api/notes", json={"text": ""})
        assert r.status_code == 422
