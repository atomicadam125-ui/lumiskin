from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from api.deps import get_current_user, get_storage_service
from controllers.photo_controller import PhotoController
from db.session import get_db
from models.photo import Photo
from models.user import User
from schemas.photo import PhotoRead
from services.image_storage_service import LocalImageStorageService

router = APIRouter()


@router.post("/images", response_model=PhotoRead, status_code=201)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    storage: LocalImageStorageService = Depends(get_storage_service),
) -> Photo:
    return await PhotoController(db, storage).upload_image(current_user, file)
