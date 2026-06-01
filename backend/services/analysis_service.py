from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.analysis import Analysis
from models.photo import Photo
from models.questionnaire import Questionnaire
from models.user import User
from schemas.skin_analysis import SkinAnalysisResult
from services.image_storage_service import LocalImageStorageService
from services.openai_service import PROMPT_VERSION, OpenAISkinAnalysisClient


class AnalysisService:
    def __init__(
        self,
        db: Session,
        storage: LocalImageStorageService,
        analyzer: OpenAISkinAnalysisClient,
    ):
        self.db = db
        self.storage = storage
        self.analyzer = analyzer

    def create(
        self,
        user: User,
        photo_id: UUID,
        questionnaire_id: UUID | None,
        photo_ids: list[UUID] | None = None,
    ) -> Analysis:
        photos = self._get_photos(user, photo_id, photo_ids)
        questionnaire = self._get_questionnaire(user, questionnaire_id)
        image_payloads = [
            (self.storage.read_image(photo.s3_key), photo.content_type) for photo in photos
        ]
        openai_result = self.analyzer.analyze(
            image_payloads,
            self._questionnaire_payload(questionnaire),
        )

        analysis = Analysis(
            user_id=user.id,
            photo_id=photos[0].id,
            photo_ids=[str(photo.id) for photo in photos],
            questionnaire_id=questionnaire.id if questionnaire else None,
            status="completed",
            scores=self._scores_for_app(openai_result),
            skin_profile=self._skin_profile(openai_result, questionnaire),
            model_versions={
                "analysis_provider": "openai",
                "openai_model": self.analyzer.model,
                "prompt_version": PROMPT_VERSION,
            },
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    @staticmethod
    def list_for_user(db: Session, user: User) -> list[Analysis]:
        return list(
            db.scalars(
                select(Analysis)
                .where(Analysis.user_id == user.id)
                .order_by(Analysis.created_at.desc())
            )
        )

    def _get_photos(
        self,
        user: User,
        photo_id: UUID,
        photo_ids: list[UUID] | None,
    ) -> list[Photo]:
        ids = photo_ids or [photo_id]
        if str(photo_id) not in {str(item) for item in ids}:
            ids = [photo_id, *ids]

        photos: list[Photo] = []
        for item in ids:
            photo = self.db.get(Photo, item)
            if photo is None or photo.user_id != user.id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
            photos.append(photo)
        return photos

    def _get_questionnaire(
        self,
        user: User,
        questionnaire_id: UUID | None,
    ) -> Questionnaire | None:
        if questionnaire_id is None:
            return None
        questionnaire = self.db.get(Questionnaire, questionnaire_id)
        if questionnaire is None or questionnaire.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Questionnaire not found",
            )
        return questionnaire

    def _questionnaire_payload(self, questionnaire: Questionnaire | None) -> dict[str, Any] | None:
        if questionnaire is None:
            return None
        return {
            "skin_type": questionnaire.skin_type,
            "sensitivity_level": questionnaire.sensitivity_level,
            "acne_frequency": questionnaire.acne_frequency,
            "current_products": questionnaire.current_products,
            "allergies": questionnaire.allergies,
            "sun_exposure_level": questionnaire.sun_exposure_level,
            "sleep_quality": questionnaire.sleep_quality,
            "stress_level": questionnaire.stress_level,
        }

    def _scores_for_app(self, result: SkinAnalysisResult) -> dict[str, dict[str, float | str]]:
        scores = result.scores.model_dump()
        return {
            key: {
                "score": round(value["score"] / 100, 2),
                "severity": value["severity"],
                "observation": value["observation"],
            }
            for key, value in scores.items()
        }

    def _skin_profile(
        self,
        result: SkinAnalysisResult,
        questionnaire: Questionnaire | None,
    ) -> dict[str, Any]:
        return {
            "skin_type": result.skin_type
            if result.skin_type != "unknown"
            else (questionnaire.skin_type if questionnaire else "unknown"),
            "overall_skin_score": result.overall_skin_score,
            "confidence": result.confidence,
            "primary_concerns": result.primary_concerns,
            "summary": result.objective_summary,
            "recommended_products": [item.model_dump() for item in result.recommended_products],
            "routine": [item.model_dump() for item in result.routine],
            "dermatologist_warning": result.dermatologist_warning,
            "disclaimer": result.disclaimer,
            "openai_analysis": result.model_dump(),
        }
