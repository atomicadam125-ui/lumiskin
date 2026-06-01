import json
from typing import Any

from openai import OpenAI

from core.config import settings

PROMPT_VERSION = "skincare-recommendation-v1"


class OpenAIRecommendationClient:
    def __init__(self, client: OpenAI | None = None):
        self.client = client or OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    def generate(
        self, skin_profile: dict[str, Any], questionnaire: dict[str, Any] | None
    ) -> dict[str, Any]:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You create conservative, non-diagnostic skincare recommendations. "
                        "Return JSON only with morning_routine, evening_routine, "
                        "ingredients_to_consider, "
                        "ingredients_to_avoid, explanation, and dermatologist_warning."
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
