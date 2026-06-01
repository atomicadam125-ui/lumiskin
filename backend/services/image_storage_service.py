from pathlib import Path
from uuid import UUID, uuid4

from core.config import settings


class LocalImageStorageService:
    def __init__(self, upload_dir: str | None = None):
        self.upload_dir = Path(upload_dir or settings.local_upload_dir)

    def save_user_image(self, user_id: UUID, data: bytes, content_type: str) -> str:
        extension = self._extension_for(content_type)
        key = f"users/{user_id}/photos/{uuid4()}.{extension}"
        destination = self.upload_dir / key
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return key

    def read_image(self, key: str) -> bytes:
        return (self.upload_dir / key).read_bytes()

    def delete_user_images(self, user_id: UUID) -> None:
        target = self.upload_dir / "users" / str(user_id)
        if not target.exists():
            return
        for path in sorted(target.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()

    def _extension_for(self, content_type: str) -> str:
        return {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}[content_type]
