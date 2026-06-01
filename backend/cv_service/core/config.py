from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class CVSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CV_", extra="ignore")

    app_name: str = "Skincare CV Service"
    max_image_bytes: int = 8 * 1024 * 1024
    min_face_confidence: float = 0.6
    max_faces: int = 1


@lru_cache
def get_settings() -> CVSettings:
    return CVSettings()


settings = get_settings()
