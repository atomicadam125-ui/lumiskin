from fastapi import UploadFile
from sqlalchemy.orm import Session

from models.photo import Photo
from models.user import User
from services.image_storage_service import LocalImageStorageService
from services.photo_service import PhotoService


class PhotoController:
    def __init__(self, db: Session, storage: LocalImageStorageService):
        self.service = PhotoService(db, storage)

    async def upload_image(self, user: User, file: UploadFile) -> Photo:
        return await self.service.upload(user, file)
