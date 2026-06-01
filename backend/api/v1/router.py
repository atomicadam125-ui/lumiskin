from fastapi import APIRouter

from api.v1 import analyses, auth, history, questionnaires, recommendations, uploads

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(questionnaires.router, prefix="/questionnaires", tags=["questionnaires"])
api_router.include_router(analyses.router, prefix="/analyses", tags=["analyses"])
api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["recommendations"]
)
api_router.include_router(history.router, prefix="/history", tags=["history"])
