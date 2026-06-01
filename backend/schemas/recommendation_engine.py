from typing import Literal

from pydantic import BaseModel, Field

Gender = Literal["female", "male", "non_binary", "prefer_not_to_say", "other"]
SkinType = Literal["oily", "dry", "combination", "normal", "sensitive"]
ConsultationLevel = Literal["routine", "consider", "recommended", "urgent"]
SkinTier = Literal[
    "Exceptional",
    "Excellent",
    "Healthy",
    "Average",
    "Needs Improvement",
    "Significant Concerns",
]


class RecommendationInput(BaseModel):
    age: int = Field(ge=13, le=100)
    gender: Gender
    skin_type: SkinType
    goals: list[str] = Field(default_factory=list, max_length=8)
    acne_score: int = Field(ge=0, le=100)
    redness_score: int = Field(ge=0, le=100)
    pigmentation_score: int = Field(ge=0, le=100)
    wrinkle_score: int = Field(ge=0, le=100)
    oiliness_score: int = Field(ge=0, le=100)
    dryness_score: int = Field(ge=0, le=100)


class RoutineStep(BaseModel):
    step: int
    category: str
    recommendation: str
    frequency: str
    rationale: str
    product_name: str | None = None
    brand: str | None = None
    product_url: str | None = None
    how_to_use: str | None = None
    caution: str | None = None


class IngredientRecommendation(BaseModel):
    ingredient: str
    why: str
    how_to_use: str


class ProductRecommendation(BaseModel):
    name: str
    brand: str
    category: str
    step: str
    url: str
    why: str
    how_to_use: str
    caution: str | None = None


class RecommendedProduct(BaseModel):
    product_name: str
    brand: str
    category: str
    step: str
    url: str
    why_chosen: str
    how_often: str
    caution: str | None = None


class AvoidIngredient(BaseModel):
    ingredient: str
    reason: str


class WarningItem(BaseModel):
    title: str
    message: str
    severity: Literal["info", "caution", "important"]


class DermatologistConsultation(BaseModel):
    level: ConsultationLevel
    rationale: str


class CategoryScores(BaseModel):
    acne_control: int = Field(ge=0, le=100)
    oil_balance: int = Field(ge=0, le=100)
    pigmentation_evenness: int = Field(ge=0, le=100)
    texture_smoothness: int = Field(ge=0, le=100)
    hydration_barrier: int = Field(ge=0, le=100)


class SkinScore(BaseModel):
    overall_skin_score: int = Field(ge=0, le=100)
    category_scores: CategoryScores
    current_tier: SkinTier


class TimelinePhase(BaseModel):
    phase: str
    expected_changes: list[str]


class ImprovementPotential(BaseModel):
    estimated_potential_score_range: str
    estimated_30_day_score_increase: int
    estimated_day_30_score: int
    estimated_timeline: list[TimelinePhase]
    note: str


class SkinSnapshot(BaseModel):
    headline: str
    skin_type: SkinType
    score: SkinScore
    confidence: int = Field(ge=0, le=100)


class WhatWeSeeItem(BaseModel):
    observation: str
    reasoning: str


class ImprovementOpportunity(BaseModel):
    concern: str
    why_it_matters: str
    priority: int


class NinetyDayPlan(BaseModel):
    phase: str
    focus: str
    actions: list[str]


class ExpectedResults(BaseModel):
    short_term: str
    medium_term: str
    long_term: str
    realistic_outcome: str


class AIConfidence(BaseModel):
    score: int = Field(ge=0, le=100)
    explanation: str


class ThirtyDayProgress(BaseModel):
    current_score: int = Field(ge=0, le=100)
    estimated_score_increase: int = Field(ge=0, le=100)
    estimated_day_30_score: int = Field(ge=0, le=100)
    focus: str
    explanation: str


class RecommendationEngineResponse(BaseModel):
    skin_snapshot: SkinSnapshot
    scores: SkinScore
    current_skin_tier: SkinTier
    what_we_see: list[WhatWeSeeItem]
    biggest_improvement_opportunities: list[ImprovementOpportunity]
    ninety_day_plan: list[NinetyDayPlan]
    timeline: list[TimelinePhase]
    thirty_day_progress: ThirtyDayProgress
    expected_results: ExpectedResults
    improvement_potential: ImprovementPotential
    ai_confidence: AIConfidence
    recommended_products: list[RecommendedProduct]
    warnings: list[WarningItem]
    disclaimer: str
    skin_summary: str
    top_concerns: list[str]
    morning_routine: list[RoutineStep]
    evening_routine: list[RoutineStep]
    product_recommendations: list[ProductRecommendation]
    ingredient_recommendations: list[IngredientRecommendation]
    ingredients_to_avoid: list[AvoidIngredient]
    lifestyle_suggestions: list[str]
    dermatologist_consultation: DermatologistConsultation
    medical_disclaimer: str
