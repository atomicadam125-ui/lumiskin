from fastapi.testclient import TestClient


def test_register_login_and_me(client: TestClient) -> None:
    register_response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@example.com", "password": "strong-password", "full_name": "Test User"},
    )
    assert register_response.status_code == 201
    assert register_response.json()["email"] == "user@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "strong-password"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_response.status_code == 200
    assert me_response.json()["full_name"] == "Test User"


def test_duplicate_registration_is_rejected(client: TestClient) -> None:
    payload = {"email": "user@example.com", "password": "strong-password"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409


def test_user_can_delete_account_in_app(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={"email": "delete@example.com", "password": "strong-password"},
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "delete@example.com", "password": "strong-password"},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    delete_response = client.delete("/api/v1/auth/me", headers=headers)
    assert delete_response.status_code == 204

    me_response = client.get("/api/v1/auth/me", headers=headers)
    assert me_response.status_code == 401

    login_again_response = client.post(
        "/api/v1/auth/login",
        json={"email": "delete@example.com", "password": "strong-password"},
    )
    assert login_again_response.status_code == 401
