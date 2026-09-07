from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_user_can_access_own_profile():
    response = client.get(
        "/users/1",
        headers={"X-Token": "alice-token"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "alice"


def test_user_cannot_access_other_user_profile():
    response = client.get(
        "/users/2",
        headers={"X-Token": "alice-token"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


def test_admin_can_access_other_user_profile():
    response = client.get(
        "/users/2",
        headers={"X-Token": "admin-token"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "bob"


def test_sql_injection_is_blocked():
    payload = "' OR 1=1 -- "

    response = client.get(
        "/products",
        params={"search": payload},
    )

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 0


def test_command_injection_is_blocked():
    payload = "127.0.0.1; id"

    response = client.get(
        "/ping",
        params={"host": payload},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid IP address"
