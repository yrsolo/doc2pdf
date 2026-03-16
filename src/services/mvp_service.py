from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from src.schemas import ConversionRequest, MvpUploadResponse
from src.services.conversion_service import ConversionService
from src.services.object_storage_service import ObjectStorageService


class MvpService:
    def __init__(
        self,
        conversion_service: ConversionService,
        object_storage_service: ObjectStorageService,
    ) -> None:
        self.conversion_service = conversion_service
        self.object_storage_service = object_storage_service

    async def convert_uploaded_file(self, filename: str, content: bytes) -> MvpUploadResponse:
        source_object_key, source_url = self.object_storage_service.upload_source_file(
            filename=filename,
            content=content,
        )
        preview_object_key, target_url, preview_url = (
            self.object_storage_service.prepare_preview_target(filename)
        )
        attachment_id = f"mvp-{uuid4().hex}"
        target_filename = f"{Path(filename).stem or 'preview'}.pdf"

        conversion_response = await self.conversion_service.convert_doc_to_pdf(
            ConversionRequest(
                attachment_id=attachment_id,
                source_url=source_url,
                target_url=target_url,
                source_filename=filename,
                target_filename=target_filename,
                request_id=attachment_id,
            )
        )

        if conversion_response.status == "failed":
            return MvpUploadResponse(
                status="failed",
                attachment_id=attachment_id,
                filename=filename,
                source_object_key=source_object_key,
                preview_object_key=preview_object_key,
                error_code=conversion_response.error_code,
                error_message=conversion_response.error_message,
            )

        return MvpUploadResponse(
            status="ready",
            attachment_id=attachment_id,
            filename=filename,
            preview_url=preview_url,
            preview_size_bytes=conversion_response.preview_size_bytes,
            source_object_key=source_object_key,
            preview_object_key=preview_object_key,
        )
