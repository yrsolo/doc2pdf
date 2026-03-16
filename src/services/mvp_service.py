from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from src.schemas import MvpPrepareUploadResponse, ConversionRequest, MvpUploadResponse
from src.services.conversion_service import ConversionService
from src.services.object_storage_service import ObjectStorageService
from src.services.mvp_token_service import MvpTokenService


class MvpService:
    def __init__(
        self,
        conversion_service: ConversionService,
        object_storage_service: ObjectStorageService,
        token_service: MvpTokenService,
    ) -> None:
        self.conversion_service = conversion_service
        self.object_storage_service = object_storage_service
        self.token_service = token_service

    def prepare_upload(
        self,
        filename: str,
        content_type: str | None = None,
    ) -> MvpPrepareUploadResponse:
        attachment_id = f"mvp-{uuid4().hex}"
        target_filename = f"{Path(filename).stem or 'preview'}.pdf"
        source_object_key, upload_url, upload_headers = (
            self.object_storage_service.prepare_source_upload(
                filename=filename,
                content_type=content_type,
            )
        )
        preview_object_key, _, preview_url = self.object_storage_service.prepare_preview_target(
            filename
        )
        conversion_token = self.token_service.issue(
            {
                "attachment_id": attachment_id,
                "filename": filename,
                "source_object_key": source_object_key,
                "preview_object_key": preview_object_key,
                "target_filename": target_filename,
            }
        )

        return MvpPrepareUploadResponse(
            status="prepared",
            filename=filename,
            source_object_key=source_object_key,
            preview_object_key=preview_object_key,
            upload_url=upload_url,
            upload_headers=upload_headers,
            preview_url=preview_url,
            conversion_token=conversion_token,
        )

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

    async def convert_prepared_upload(self, conversion_token: str) -> MvpUploadResponse:
        payload = self.token_service.verify(conversion_token)
        source_object_key = payload["source_object_key"]
        preview_object_key = payload["preview_object_key"]
        filename = payload["filename"]
        attachment_id = payload["attachment_id"]
        target_filename = payload["target_filename"]
        source_url = self.object_storage_service.generate_get_url(source_object_key)
        target_url = self.object_storage_service.generate_put_url(
            object_key=preview_object_key,
            content_type="application/pdf",
            content_disposition=f'inline; filename="{target_filename}"',
        )
        preview_url = self.object_storage_service.generate_get_url(preview_object_key)

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
