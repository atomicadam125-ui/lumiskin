from fastapi.testclient import TestClient


def test_recommendation_engine_returns_structured_cosmetic_guidance(client: TestClient) -> None:
    response = client.post(
        "/api/v1/recommendations/generate",
        json={
            "age": 28,
            "gender": "female",
            "skin_type": "combination",
            "goals": ["reduce acne", "brighten skin"],
            "acne_score": 72,
            "redness_score": 30,
            "pigmentation_score": 40,
            "wrinkle_score": 15,
            "oiliness_score": 70,
            "dryness_score": 20,
        },
    )

    assert response.status_code == 200
    body = response.json()
    expected_display_keys = {
        "skin_snapshot",
        "scores",
        "current_skin_tier",
        "improvement_potential",
        "timeline",
        "thirty_day_progress",
        "morning_routine",
        "evening_routine",
        "recommended_products",
        "warnings",
        "disclaimer",
    }
    assert expected_display_keys.issubset(body)
    assert body["skin_snapshot"]["score"]["overall_skin_score"] >= 0
    assert body["skin_snapshot"]["score"]["overall_skin_score"] <= 100
    assert body["scores"] == body["skin_snapshot"]["score"]
    assert body["current_skin_tier"] == body["scores"]["current_tier"]
    assert body["skin_snapshot"]["score"]["current_tier"] in {
        "Exceptional",
        "Excellent",
        "Healthy",
        "Average",
        "Needs Improvement",
        "Significant Concerns",
    }
    assert set(body["skin_snapshot"]["score"]["category_scores"]) == {
        "acne_control",
        "oil_balance",
        "pigmentation_evenness",
        "texture_smoothness",
        "hydration_barrier",
    }
    assert body["improvement_potential"]["estimated_potential_score_range"]
    expected_30_day_lift = 6
    assert body["improvement_potential"]["estimated_30_day_score_increase"] == expected_30_day_lift
    assert body["improvement_potential"]["estimated_day_30_score"] == (
        body["scores"]["overall_skin_score"] + expected_30_day_lift
    )
    assert body["thirty_day_progress"]["estimated_score_increase"] == expected_30_day_lift
    assert body["thirty_day_progress"]["estimated_day_30_score"] == (
        body["scores"]["overall_skin_score"] + expected_30_day_lift
    )
    assert "AI-estimated" in body["thirty_day_progress"]["explanation"]
    assert [phase["phase"] for phase in body["improvement_potential"]["estimated_timeline"]] == [
        "2-4 weeks",
        "6-8 weeks",
        "3-6 months",
    ]
    assert body["timeline"] == body["improvement_potential"]["estimated_timeline"]
    assert "not a medical guarantee" in body["improvement_potential"]["note"]
    assert "flawless skin" not in str(body).lower()
    assert "clearer, smoother, more even-looking skin" in body["expected_results"]["long_term"]
    assert body["top_concerns"][0] == "acne and congestion"
    assert body["dermatologist_consultation"]["level"] == "consider"
    assert "medical diagnosis" in body["medical_disclaimer"]
    assert len(body["morning_routine"]) == 4
    assert len(body["evening_routine"]) == 4
    assert any(step["product_name"] for step in body["morning_routine"])
    assert any("Retinol" in step["recommendation"] for step in body["evening_routine"])
    assert any("retinol" in item["ingredient"] for item in body["ingredient_recommendations"])
    assert any(
        item["ingredient"] == "salicylic acid" for item in body["ingredient_recommendations"]
    )
    assert any("Beauty of Joseon" in item["brand"] for item in body["product_recommendations"])
    assert any("retinol" in item["category"] for item in body["product_recommendations"])
    assert all(item["url"].startswith("https://") for item in body["product_recommendations"])
    assert body["recommended_products"]
    for product in body["recommended_products"]:
        assert product["product_name"]
        assert product["step"]
        assert product["why_chosen"]
        assert product["how_often"]
        assert "caution" in product
    assert body["warnings"]
    assert any("purge" in warning["message"] for warning in body["warnings"])
    assert "diagnose" not in body["skin_summary"].lower()
