from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RecommendationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    analysis_id: UUID
    routine: dict[str, Any]
    explanation: str | None
    llm_model: str
    prompt_version: str
    created_at: datetime
