import json

import httpx

from src.config import settings
from src.schemas import ConversionRequest, ConversionResponse


class GotenbergClient:
    def __init__(
        self,
        base_url: str,
        timeout_sec: int | None = None,
        trust_env: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_sec = timeout_sec or settings.gotenberg_timeout_sec
        self.trust_env = trust_env

    async def convert_doc_to_pdf(self, request: ConversionRequest) -> ConversionResponse:
        try:
            pdf_bytes = await self._render_pdf(request)
            await self._upload_pdf(request, pdf_bytes)
        except httpx.HTTPStatusError as exc:
            return ConversionResponse(
                status="failed",
                attachment_id=request.attachment_id,
                error_code="upstream_http_error",
                error_message=self._format_http_error(exc),
            )
        except httpx.HTTPError as exc:
            return ConversionResponse(
                status="failed",
                attachment_id=request.attachment_id,
                error_code="network_error",
                error_message=str(exc),
            )
        except Exception as exc:  # pragma: no cover - defensive fallback
            return ConversionResponse(
                status="failed",
                attachment_id=request.attachment_id,
                error_code="internal_error",
                error_message=str(exc),
            )

        return ConversionResponse(
            status="ready",
            attachment_id=request.attachment_id,
            preview_size_bytes=len(pdf_bytes),
        )

    async def _render_pdf(self, request: ConversionRequest) -> bytes:
        payload = json.dumps([{"url": str(request.source_url)}])
        headers = {}
        if request.request_id:
            headers["X-Request-Id"] = request.request_id

        async with httpx.AsyncClient(
            timeout=self.timeout_sec,
            trust_env=self.trust_env,
        ) as client:
            response = await client.post(
                f"{self.base_url}/forms/libreoffice/convert",
                files={
                    "downloadFrom": (None, payload),
                    "outputFilename": (None, request.target_filename),
                },
                headers=headers,
            )
            response.raise_for_status()
            return response.content

    async def _upload_pdf(self, request: ConversionRequest, pdf_bytes: bytes) -> None:
        headers = {
            "Content-Type": "application/pdf",
            "Content-Disposition": f'inline; filename="{request.target_filename}"',
        }
        if request.request_id:
            headers["X-Request-Id"] = request.request_id

        async with httpx.AsyncClient(
            timeout=self.timeout_sec,
            trust_env=self.trust_env,
        ) as client:
            response = await client.put(
                str(request.target_url),
                content=pdf_bytes,
                headers=headers,
            )
            response.raise_for_status()

    @staticmethod
    def _format_http_error(exc: httpx.HTTPStatusError) -> str:
        response = exc.response
        request = response.request
        return (
            f"{request.method} {request.url} returned {response.status_code}: "
            f"{response.text[:500]}"
        )
