import base64
import json
from typing import Any

from fastapi import HTTPException, status
from openai import OpenAI

from core.config import settings
from schemas.skin_analysis import SkinAnalysisResult

PROMPT_VERSION = "openai-skin-analysis-v1"


class OpenAISkinAnalysisClient:
    def __init__(self, client: OpenAI | None = None):
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OPENAI_API_KEY is not configured",
            )
        self.client = client or OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def analyze(
        self,
        images: list[tuple[bytes, str]],
        questionnaire: dict[str, Any] | None,
    ) -> SkinAnalysisResult:
        content: list[dict[str, Any]] = [
            {
                "type": "input_text",
                "text": (
                    "Analyze the user's cosmetic skin condition from the submitted face photos. "
                    "Use objective, standardized language. Do not diagnose disease. Score visible "
                    "cosmetic concerns from 0 to 100 where 0 is not visible and 100 is severe. "
                    "Recommend only high-quality Korean skincare products or product categories "
                    "that fit the visible concerns and questionnaire. Include conservative usage "
                    "instructions and cautions for actives."
                ),
            },
            {
                "type": "input_text",
                "text": json.dumps({"questionnaire": questionnaire or {}}, default=str),
            },
        ]
        for image_bytes, content_type in images:
            content.append(
                {
                    "type": "input_image",
                    "image_url": self._data_url(image_bytes, content_type),
                    "detail": "high",
                }
            )

        response = self.client.responses.parse(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are a conservative cosmetic skincare analysis assistant. "
                        "You provide structured, repeatable observations from images and user "
                        "questionnaire data. You are not a medical device, do not diagnose, and "
                        "advise dermatology care for painful, rapidly changing, severe, or "
                        "persistent concerns."
                    ),
                },
                {"role": "user", "content": content},
            ],
            text_format=SkinAnalysisResult,
        )
        if response.output_parsed is None:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="OpenAI did not return a structured skin analysis",
            )
        return response.output_parsed

    def _data_url(self, image_bytes: bytes, content_type: str) -> str:
        encoded = base64.b64encode(image_bytes).decode("ascii")
        return f"data:{content_type};base64,{encoded}"


class OpenAIRecommendationClient:
    def __init__(self, client: OpenAI | None = None):
        if not settings.openai_api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OPENAI_API_KEY is not configured",
            )
        self.client = client or OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate(
        self, skin_profile: dict[str, Any], questionnaire: dict[str, Any] | None
    ) -> dict[str, Any]:
        existing = skin_profile.get("openai_analysis")
        if isinstance(existing, dict):
            return existing

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Create conservative, non-diagnostic Korean skincare recommendations. "
                        "Return JSON only with morning_routine, evening_routine, "
                        "ingredients_to_consider, ingredients_to_avoid, explanation, and "
                        "dermatologist_warning."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {"skin_profile": skin_profile, "questionnaire": questionnaire},
                        default=str,
                    ),
                },
            ],
        )
        return json.loads(response.output_text)
