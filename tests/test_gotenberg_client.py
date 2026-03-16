import asyncio

import httpx

from src.schemas import ConversionRequest
from src.services.gotenberg_client import GotenbergClient


def test_gotenberg_client_converts_and_uploads_pdf():
    captured = {"convert_body": None, "uploaded_pdf": None, "request_ids": []}

    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/forms/libreoffice/convert":
            body = (await request.aread()).decode()
            captured["convert_body"] = body
            captured["request_ids"].append(request.headers.get("X-Request-Id"))
            return httpx.Response(200, content=b"%PDF-1.7 fake")

        if request.url.path == "/upload/preview.pdf":
            captured["uploaded_pdf"] = await request.aread()
            captured["request_ids"].append(request.headers.get("X-Request-Id"))
            return httpx.Response(200)

        return httpx.Response(404)

    transport = httpx.MockTransport(handler)
    original_async_client = httpx.AsyncClient

    def fake_async_client(*args, **kwargs):
        kwargs["transport"] = transport
        return original_async_client(*args, **kwargs)

    httpx.AsyncClient = fake_async_client
    try:
        client = GotenbergClient(base_url="https://gotenberg.local", timeout_sec=5)
        response = asyncio.run(
            client.convert_doc_to_pdf(
                ConversionRequest(
                    attachment_id="att_123",
                    source_url="https://storage.local/source.doc",
                    target_url="https://storage.local/upload/preview.pdf",
                    source_filename="source.doc",
                    target_filename="preview.pdf",
                    request_id="req-123",
                )
            )
        )
    finally:
        httpx.AsyncClient = original_async_client

    assert response.status == "ready"
    assert response.preview_size_bytes == len(b"%PDF-1.7 fake")
    assert 'name="downloadFrom"' in captured["convert_body"]
    assert '[{"url": "https://storage.local/source.doc"}]' in captured["convert_body"]
    assert 'name="outputFilename"' in captured["convert_body"]
    assert "preview.pdf" in captured["convert_body"]
    assert captured["uploaded_pdf"] == b"%PDF-1.7 fake"
    assert captured["request_ids"] == ["req-123", "req-123"]


def test_gotenberg_client_normalizes_upstream_failures():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(502, text="bad gateway", request=request)

    transport = httpx.MockTransport(handler)
    original_async_client = httpx.AsyncClient

    def fake_async_client(*args, **kwargs):
        kwargs["transport"] = transport
        return original_async_client(*args, **kwargs)

    httpx.AsyncClient = fake_async_client
    try:
        client = GotenbergClient(base_url="https://gotenberg.local", timeout_sec=5)
        response = asyncio.run(
            client.convert_doc_to_pdf(
                ConversionRequest(
                    attachment_id="att_123",
                    source_url="https://storage.local/source.doc",
                    target_url="https://storage.local/upload/preview.pdf",
                    source_filename="source.doc",
                )
            )
        )
    finally:
        httpx.AsyncClient = original_async_client

    assert response.status == "failed"
    assert response.error_code == "upstream_http_error"
    assert "502" in response.error_message
