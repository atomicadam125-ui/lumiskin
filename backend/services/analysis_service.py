from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.photo import Photo
from models.questionnaire import Questionnaire
from models.user import User


class AnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user: User,
        photo_id: UUID,
        questionnaire_id: UUID | None,
        photo_ids: list[UUID] | None = None,
        scores: dict | None = None,
        model_versions: dict[str, str] | None = None,
    ) -> Analysis:
        photo = self.db.get(Photo, photo_id)
        if photo is None or photo.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

        questionnaire = None
        if questionnaire_id is not None:
            questionnaire = self.db.get(Questionnaire, questionnaire_id)
            if questionnaire is None or questionnaire.user_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Questionnaire not found"
                )

        for extra_photo_id in photo_ids or []:
            extra_photo = self.db.get(Photo, extra_photo_id)
            if extra_photo is None or extra_photo.user_id != user.id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")

        normalized_scores = self._normalize_scores(scores) if scores else self._placeholder_scores()
        skin_profile = self._build_skin_profile(normalized_scores, questionnaire)
        analysis = Analysis(
            user_id=user.id,
            photo_id=photo.id,
            photo_ids=[str(item) for item in (photo_ids or [photo.id])],
            questionnaire_id=questionnaire.id if questionnaire else None,
            status="completed",
            scores=normalized_scores,
            skin_profile=skin_profile,
            model_versions=model_versions or {"skin_baseline": "placeholder-v1"},
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def _normalize_scores(self, scores: dict) -> dict[str, dict[str, float | str]]:
        mapping = {
            "acne_score": "acne",
            "redness_score": "redness",
            "pigmentation_score": "hyperpigmentation",
            "wrinkle_score": "fine_lines",
            "oiliness_score": "oiliness",
            "dryness_score": "dryness",
        }
        normalized = {}
        for source_key, target_key in mapping.items():
            raw_value = scores.get(source_key)
            if raw_value is None:
                continue
            value = max(0.0, min(100.0, float(raw_value))) / 100.0
            normalized[target_key] = {"score": value, "severity": self._severity(value)}

        return {**self._placeholder_scores(), **normalized}

    def _severity(self, value: float) -> str:
        if value >= 0.75:
            return "high"
        if value >= 0.45:
            return "moderate"
        if value >= 0.2:
            return "mild"
        return "low"

    def list_for_user(self, user: User) -> list[Analysis]:
        return list(
            self.db.scalars(
                select(Analysis)
                .where(Analysis.user_id == user.id)
                .order_by(Analysis.created_at.desc())
            )
        )

    def _placeholder_scores(self) -> dict[str, dict[str, float | str]]:
        return {
            "acne": {"score": 0.18, "severity": "low"},
            "redness": {"score": 0.24, "severity": "mild"},
            "hyperpigmentation": {"score": 0.21, "severity": "mild"},
            "fine_lines": {"score": 0.16, "severity": "low"},
            "pores": {"score": 0.32, "severity": "mild"},
            "oiliness": {"score": 0.28, "severity": "mild"},
            "dryness": {"score": 0.22, "severity": "mild"},
        }

    def _build_skin_profile(
        self,
        scores: dict[str, dict[str, float | str]],
        questionnaire: Questionnaire | None,
    ) -> dict[str, object]:
        concerns = [name for name, result in scores.items() if float(result["score"]) >= 0.3]
        return {
            "skin_type": questionnaire.skin_type if questionnaire else "unknown",
            "primary_concerns": concerns,
            "sensitivity_level": questionnaire.sensitivity_level if questionnaire else None,
            "summary": "Initial computer-vision baseline pending production model integration.",
        }
