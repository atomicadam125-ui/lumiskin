from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PhotoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    s3_key: str
    original_filename: str | None
    content_type: str
    size_bytes: int
    image_width: int | None
    image_height: int | None
    created_at: datetime
