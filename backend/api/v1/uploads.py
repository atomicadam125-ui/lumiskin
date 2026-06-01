from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from api.deps import get_current_user, get_storage_service
from db.session import get_db
from models.photo import Photo
from models.user import User
from schemas.photo import PhotoRead
from services.photo_service import PhotoService
from services.s3_service import S3StorageService

router = APIRouter()


@router.post("/images", response_model=PhotoRead, status_code=201)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    storage: S3StorageService = Depends(get_storage_service),
) -> Photo:
    return await PhotoService(db, storage).upload(current_user, file)
