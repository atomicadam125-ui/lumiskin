import os
from collections.abc import Generator
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("SECRET_KEY", "test-secret-key-that-is-long-enough-for-jwt")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite://")
os.environ.setdefault("S3_BUCKET_NAME", "test-bucket")
os.environ.setdefault("OPENAI_API_KEY", "test-key")

import models  # noqa: F401, E402
from api.deps import get_recommendation_client, get_storage_service  # noqa: E402
from db.base import Base  # noqa: E402
from db.session import get_db  # noqa: E402
from main import create_app  # noqa: E402


class FakeStorageService:
    def upload_user_image(self, user_id: UUID, data: bytes, content_type: str) -> str:
        return f"users/{user_id}/photos/fake-image.jpg"

    def delete_user_images(self, user_id: UUID) -> None:
        return None


class FakeRecommendationClient:
    model = "fake-llm"

    def generate(self, skin_profile: dict, questionnaire: dict | None) -> dict:
        return {
            "morning_routine": [
                {"step": 1, "category": "cleanser", "recommendation": "Gentle cleanser"}
            ],
            "evening_routine": [
                {"step": 1, "category": "moisturizer", "recommendation": "Barrier cream"}
            ],
            "ingredients_to_consider": ["niacinamide"],
            "ingredients_to_avoid": ["harsh scrubs"],
            "explanation": "A conservative starter routine based on the current profile.",
            "dermatologist_warning": (
                "Consult a dermatologist for painful, worsening, or persistent symptoms."
            ),
        }


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
    )
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
        yield session

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app = create_app()

    def override_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_storage_service] = FakeStorageService
    app.dependency_overrides[get_recommendation_client] = FakeRecommendationClient

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
