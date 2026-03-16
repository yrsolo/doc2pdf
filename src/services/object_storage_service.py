from __future__ import annotations

import mimetypes
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import boto3
from botocore.client import Config

from src.config import settings


class ObjectStorageService:
    def __init__(self) -> None:
        if not settings.aws_access_key_id or not settings.aws_secret_access_key:
            raise ValueError("Object Storage credentials are not configured.")

        self.bucket = settings.object_storage_bucket
        self.prefix = settings.object_storage_prefix.strip("/")
        self.presign_ttl_sec = settings.object_storage_presign_ttl_sec
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.object_storage_endpoint,
            region_name=settings.object_storage_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            config=Config(signature_version="s3v4"),
        )

    def upload_source_file(self, filename: str, content: bytes) -> tuple[str, str]:
        object_key = self._build_object_key("uploads", filename)
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        self.client.upload_fileobj(
            Fileobj=BytesIO(content),
            Bucket=self.bucket,
            Key=object_key,
            ExtraArgs={
                "ContentType": content_type,
                "ContentDisposition": f'attachment; filename="{Path(filename).name}"',
            },
        )
        return object_key, self.generate_get_url(object_key)

    def prepare_source_upload(
        self,
        filename: str,
        content_type: str | None = None,
    ) -> tuple[str, str, dict[str, str]]:
        object_key = self._build_object_key("uploads", filename)
        effective_content_type = (
            content_type or mimetypes.guess_type(filename)[0] or "application/octet-stream"
        )
        upload_headers = {
            "Content-Type": effective_content_type,
            "Content-Disposition": f'attachment; filename="{Path(filename).name}"',
        }
        put_url = self.generate_put_url(
            object_key=object_key,
            content_type=effective_content_type,
            content_disposition=upload_headers["Content-Disposition"],
        )
        return object_key, put_url, upload_headers

    def prepare_preview_target(self, filename: str) -> tuple[str, str, str]:
        object_key = self._build_object_key("previews", filename, extension=".pdf")
        put_url = self.generate_put_url(
            object_key=object_key,
            content_type="application/pdf",
            content_disposition=f'inline; filename="{Path(filename).stem or "preview"}.pdf"',
        )
        get_url = self.generate_get_url(object_key)
        return object_key, put_url, get_url

    def generate_get_url(self, object_key: str) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": object_key},
            ExpiresIn=self.presign_ttl_sec,
        )

    def generate_put_url(
        self,
        object_key: str,
        content_type: str | None = None,
        content_disposition: str | None = None,
    ) -> str:
        params: dict[str, str] = {"Bucket": self.bucket, "Key": object_key}
        if content_type:
            params["ContentType"] = content_type
        if content_disposition:
            params["ContentDisposition"] = content_disposition
        return self.client.generate_presigned_url(
            ClientMethod="put_object",
            Params=params,
            ExpiresIn=self.presign_ttl_sec,
        )

    def _build_object_key(
        self,
        category: str,
        filename: str,
        extension: str | None = None,
    ) -> str:
        sanitized_name = Path(filename).stem.replace(" ", "_")
        ext = extension or Path(filename).suffix or ".bin"
        object_name = f"{uuid4().hex}-{sanitized_name}{ext}"
        if self.prefix:
            return f"{self.prefix}/{category}/{object_name}"
        return f"{category}/{object_name}"
