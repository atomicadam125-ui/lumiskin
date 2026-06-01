from uuid import UUID, uuid4

import boto3
from botocore.client import BaseClient

from core.config import settings


class S3StorageService:
    def __init__(self, client: BaseClient | None = None):
        self.client = None
        if settings.storage_backend == "s3":
            self.client = client or boto3.client(
                "s3",
                region_name=settings.aws_region,
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
            )
        self.bucket = settings.s3_bucket_name

    def upload_user_image(self, user_id: UUID, data: bytes, content_type: str) -> str:
        extension = _extension_for_content_type(content_type)
        key = f"users/{user_id}/photos/{uuid4()}.{extension}"
        if settings.storage_backend == "local":
            self._write_local(key, data)
            return key

        if self.client is None:
            raise RuntimeError("S3 client is not configured")

        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            ContentType=content_type,
            ServerSideEncryption="AES256",
        )
        return key

    def delete_user_images(self, user_id: UUID) -> None:
        prefix = f"users/{user_id}/photos/"
        if settings.storage_backend == "local":
            self._delete_local_prefix(prefix)
            return

        if self.client is None:
            raise RuntimeError("S3 client is not configured")

        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            objects = [{"Key": item["Key"]} for item in page.get("Contents", [])]
            if objects:
                self.client.delete_objects(Bucket=self.bucket, Delete={"Objects": objects})

    def _write_local(self, key: str, data: bytes) -> None:
        from pathlib import Path

        destination = Path(settings.local_upload_dir) / key
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    def _delete_local_prefix(self, prefix: str) -> None:
        from pathlib import Path
        from shutil import rmtree

        target = Path(settings.local_upload_dir) / prefix
        if target.exists():
            rmtree(target)


def _extension_for_content_type(content_type: str) -> str:
    return {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
    }.get(content_type, "bin")
