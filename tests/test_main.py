from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_returns_hello_world():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello World"}


def test_unknown_route_returns_404():
    r = client.get("/does-not-exist")
    assert r.status_code == 404


def test_openapi_schema_is_served():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    assert "/" in r.json()["paths"]
