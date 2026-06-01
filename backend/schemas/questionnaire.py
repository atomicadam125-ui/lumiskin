from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

SkinType = Literal["oily", "dry", "combination", "normal", "sensitive"]
Frequency = Literal["rarely", "sometimes", "often", "persistent"]


class QuestionnaireCreate(BaseModel):
    skin_type: SkinType
    sensitivity_level: int = Field(ge=1, le=5)
    acne_frequency: Frequency
    current_products: list[str] = Field(default_factory=list, max_length=30)
    allergies: list[str] = Field(default_factory=list, max_length=30)
    sun_exposure_level: int = Field(ge=1, le=5)
    sleep_quality: int = Field(ge=1, le=5)
    stress_level: int = Field(ge=1, le=5)


class QuestionnaireRead(QuestionnaireCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime
