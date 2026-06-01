from typing import Literal

from pydantic import BaseModel, Field


Severity = Literal["low", "mild", "moderate", "high"]


class ConditionScore(BaseModel):
    score: int = Field(ge=0, le=100)
    severity: Severity
    observation: str


class SkinScores(BaseModel):
    acne: ConditionScore
    redness: ConditionScore
    hyperpigmentation: ConditionScore
    fine_lines: ConditionScore
    pores: ConditionScore
    oiliness: ConditionScore
    dryness: ConditionScore


class RecommendedProduct(BaseModel):
    product_name: str
    brand: str
    category: str
    routine_step: str
    why_chosen: str
    how_to_use: str
    caution: str | None


class RoutineStep(BaseModel):
    step: int
    time_of_day: Literal["morning", "evening", "both"]
    category: str
    instruction: str
    frequency: str


class SkinAnalysisResult(BaseModel):
    overall_skin_score: int = Field(ge=0, le=100)
    skin_type: Literal["oily", "dry", "combination", "normal", "sensitive", "unknown"]
    confidence: int = Field(ge=0, le=100)
    scores: SkinScores
    primary_concerns: list[str]
    objective_summary: str
    routine: list[RoutineStep]
    recommended_products: list[RecommendedProduct]
    dermatologist_warning: str
    disclaimer: str
