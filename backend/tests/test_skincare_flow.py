from fastapi.testclient import TestClient


def auth_headers(client: TestClient) -> dict[str, str]:
    client.post(
        "/api/v1/auth/register",
        json={"email": "flow@example.com", "password": "strong-password", "full_name": "Flow User"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "flow@example.com", "password": "strong-password"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_complete_skincare_flow(client: TestClient) -> None:
    headers = auth_headers(client)

    upload_response = client.post(
        "/api/v1/uploads/images",
        headers=headers,
        files={"file": ("face.jpg", b"fake image bytes", "image/jpeg")},
    )
    assert upload_response.status_code == 201
    photo_id = upload_response.json()["id"]
    assert upload_response.json()["s3_key"].endswith("fake-image.jpg")

    questionnaire_response = client.post(
        "/api/v1/questionnaires",
        headers=headers,
        json={
            "skin_type": "combination",
            "sensitivity_level": 3,
            "acne_frequency": "sometimes",
            "current_products": ["cleanser", "sunscreen"],
            "allergies": [],
            "sun_exposure_level": 4,
            "sleep_quality": 3,
            "stress_level": 2,
        },
    )
    assert questionnaire_response.status_code == 201
    questionnaire_id = questionnaire_response.json()["id"]

    analysis_response = client.post(
        "/api/v1/analyses",
        headers=headers,
        json={"photo_id": photo_id, "questionnaire_id": questionnaire_id},
    )
    assert analysis_response.status_code == 201
    analysis = analysis_response.json()
    assert analysis["status"] == "completed"
    assert analysis["skin_profile"]["skin_type"] == "combination"

    recommendation_response = client.post(
        f"/api/v1/analyses/{analysis['id']}/recommendations",
        headers=headers,
    )
    assert recommendation_response.status_code == 201
    recommendation = recommendation_response.json()
    assert recommendation["routine"]["ingredients_to_consider"] == ["niacinamide"]

    history_response = client.get("/api/v1/history", headers=headers)
    assert history_response.status_code == 200
    history = history_response.json()
    assert len(history["photos"]) == 1
    assert len(history["questionnaires"]) == 1
    assert len(history["analyses"]) == 1
    assert len(history["recommendations"]) == 1


def test_analysis_accepts_cv_scores(client: TestClient) -> None:
    headers = auth_headers(client)
    upload_response = client.post(
        "/api/v1/uploads/images",
        headers=headers,
        files={"file": ("face.jpg", b"fake image bytes", "image/jpeg")},
    )
    photo_id = upload_response.json()["id"]

    analysis_response = client.post(
        "/api/v1/analyses",
        headers=headers,
        json={
            "photo_id": photo_id,
            "scores": {
                "acne_score": 72,
                "redness_score": 30,
                "pigmentation_score": 40,
                "wrinkle_score": 15,
                "oiliness_score": 70,
                "dryness_score": 20,
                "confidence": 88,
            },
            "model_versions": {"cv_service": "test-v1"},
        },
    )

    assert analysis_response.status_code == 201
    analysis = analysis_response.json()
    assert analysis["scores"]["acne"]["score"] == 0.72
    assert analysis["scores"]["acne"]["severity"] == "moderate"
    assert analysis["model_versions"]["cv_service"] == "test-v1"


def test_analysis_accepts_three_capture_angles(client: TestClient) -> None:
    headers = auth_headers(client)
    photo_ids = []
    for name in ["front.jpg", "left.jpg", "right.jpg"]:
      upload_response = client.post(
          "/api/v1/uploads/images",
          headers=headers,
          files={"file": (name, b"fake image bytes", "image/jpeg")},
      )
      assert upload_response.status_code == 201
      photo_ids.append(upload_response.json()["id"])

    analysis_response = client.post(
        "/api/v1/analyses",
        headers=headers,
        json={"photo_id": photo_ids[0], "photo_ids": photo_ids},
    )

    assert analysis_response.status_code == 201
    assert analysis_response.json()["photo_ids"] == photo_ids
