from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnalysisCreate(BaseModel):
    photo_id: UUID
    photo_ids: list[UUID] | None = None
    questionnaire_id: UUID | None = None
    scores: dict[str, Any] | None = None
    model_versions: dict[str, str] | None = None


class AnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    photo_id: UUID
    photo_ids: list[str]
    questionnaire_id: UUID | None
    status: str
    scores: dict[str, Any]
    skin_profile: dict[str, Any]
    model_versions: dict[str, str]
    created_at: datetime
