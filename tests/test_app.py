import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json()["message"]
    # Already signed up
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    # Unregister
    resp3 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp3.status_code == 200
    assert f"Unregistered {email}" in resp3.json()["message"]
    # Unregister again (should fail)
    resp4 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp4.status_code == 404
