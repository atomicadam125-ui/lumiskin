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
os.environ.setdefault("OPENAI_API_KEY", "test-key")

import models  # noqa: F401, E402
from api.deps import (  # noqa: E402
    get_recommendation_client,
    get_skin_analysis_client,
    get_storage_service,
)
from db.base import Base  # noqa: E402
from db.session import get_db  # noqa: E402
from main import create_app  # noqa: E402
from schemas.skin_analysis import (  # noqa: E402
    ConditionScore,
    RecommendedProduct,
    RoutineStep,
    SkinAnalysisResult,
    SkinScores,
)


class FakeStorageService:
    files: dict[str, bytes] = {}

    def save_user_image(self, user_id: UUID, data: bytes, content_type: str) -> str:
        key = f"users/{user_id}/photos/fake-image.jpg"
        self.files[key] = data
        return key

    def read_image(self, key: str) -> bytes:
        return self.files[key]

    def delete_user_images(self, user_id: UUID) -> None:
        return None


class FakeSkinAnalysisClient:
    model = "fake-vision-model"

    def analyze(
        self, images: list[tuple[bytes, str]], questionnaire: dict | None
    ) -> SkinAnalysisResult:
        assert images
        return SkinAnalysisResult(
            overall_skin_score=74,
            skin_type=questionnaire["skin_type"] if questionnaire else "unknown",
            confidence=88,
            scores=SkinScores(
                acne=ConditionScore(score=72, severity="moderate", observation="Visible blemishes"),
                redness=ConditionScore(score=30, severity="mild", observation="Mild redness"),
                hyperpigmentation=ConditionScore(
                    score=40, severity="mild", observation="Some uneven tone"
                ),
                fine_lines=ConditionScore(score=15, severity="low", observation="Minimal lines"),
                pores=ConditionScore(score=35, severity="mild", observation="Visible pores"),
                oiliness=ConditionScore(score=70, severity="moderate", observation="Shine visible"),
                dryness=ConditionScore(score=20, severity="mild", observation="Mild dryness"),
            ),
            primary_concerns=["acne", "oiliness"],
            objective_summary="Combination skin with moderate blemish and oil concerns.",
            routine=[
                RoutineStep(
                    step=1,
                    time_of_day="both",
                    category="cleanser",
                    instruction="Use a gentle low-pH cleanser.",
                    frequency="daily",
                )
            ],
            recommended_products=[
                RecommendedProduct(
                    product_name="Low pH Good Morning Gel Cleanser",
                    brand="COSRX",
                    category="cleanser",
                    routine_step="cleanse",
                    why_chosen="Gentle option for combination skin.",
                    how_to_use="Massage onto damp skin and rinse.",
                    caution=None,
                )
            ],
            dermatologist_warning="Seek dermatologist care for painful or worsening lesions.",
            disclaimer="Cosmetic analysis only; not a diagnosis.",
        )


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
    app.dependency_overrides[get_skin_analysis_client] = FakeSkinAnalysisClient
    app.dependency_overrides[get_recommendation_client] = FakeRecommendationClient

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
