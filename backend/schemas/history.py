from pydantic import BaseModel

from schemas.analysis import AnalysisRead
from schemas.photo import PhotoRead
from schemas.questionnaire import QuestionnaireRead
from schemas.recommendation import RecommendationRead


class UserHistoryRead(BaseModel):
    photos: list[PhotoRead]
    questionnaires: list[QuestionnaireRead]
    analyses: list[AnalysisRead]
    recommendations: list[RecommendationRead]
