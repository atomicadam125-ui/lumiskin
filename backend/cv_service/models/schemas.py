from pydantic import BaseModel, Field


class SkinAnalysisResponse(BaseModel):
    acne_score: int = Field(ge=0, le=100)
    redness_score: int = Field(ge=0, le=100)
    pigmentation_score: int = Field(ge=0, le=100)
    wrinkle_score: int = Field(ge=0, le=100)
    oiliness_score: int = Field(ge=0, le=100)
    dryness_score: int = Field(ge=0, le=100)
    confidence: int = Field(ge=0, le=100)
