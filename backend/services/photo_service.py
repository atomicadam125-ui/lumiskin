from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from models.photo import Photo
from models.user import User
from services.s3_service import S3StorageService

MAX_IMAGE_BYTES = 8 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


class PhotoService:
    def __init__(self, db: Session, storage: S3StorageService):
        self.db = db
        self.storage = storage

    async def upload(self, user: User, file: UploadFile) -> Photo:
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported image type"
            )

        data = await file.read()
        if not data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image is empty")
        if len(data) > MAX_IMAGE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Image is too large"
            )

        s3_key = self.storage.upload_user_image(user.id, data, file.content_type)
        photo = Photo(
            user_id=user.id,
            s3_key=s3_key,
            original_filename=file.filename,
            content_type=file.content_type,
            size_bytes=len(data),
        )
        self.db.add(photo)
        self.db.commit()
        self.db.refresh(photo)
        return photo
