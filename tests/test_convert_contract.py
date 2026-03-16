from fastapi.testclient import TestClient

from src.api import routes
from src.config import settings
from src.main import app
from src.schemas import ConversionResponse


def test_convert_endpoint_uses_json_contract():
    client = TestClient(app)
    original_token = settings.shared_token
    original_method = routes.service.convert_doc_to_pdf
    settings.shared_token = "test-shared-token"

    async def fake_convert_doc_to_pdf(request):
        return ConversionResponse(
            status="ready",
            attachment_id=request.attachment_id,
            preview_size_bytes=1234,
        )

    routes.service.convert_doc_to_pdf = fake_convert_doc_to_pdf

    try:
        response = client.post(
            "/convert/doc-to-pdf",
            headers={"X-Shared-Token": "test-shared-token"},
            json={
                "attachment_id": "att_123",
                "source_url": "https://example.com/source.doc",
                "target_url": "https://example.com/preview.pdf",
                "source_filename": "source.doc",
                "target_filename": "preview.pdf",
                "request_id": "req-123",
            },
        )
    finally:
        settings.shared_token = original_token
        routes.service.convert_doc_to_pdf = original_method

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["attachment_id"] == "att_123"
    assert body["preview_size_bytes"] == 1234


def test_convert_endpoint_rejects_missing_shared_token():
    client = TestClient(app)
    original_token = settings.shared_token
    settings.shared_token = "test-shared-token"

    try:
        response = client.post(
            "/convert/doc-to-pdf",
            json={
                "attachment_id": "att_123",
                "source_url": "https://example.com/source.doc",
                "target_url": "https://example.com/preview.pdf",
                "source_filename": "source.doc",
                "target_filename": "preview.pdf",
            },
        )
    finally:
        settings.shared_token = original_token

    assert response.status_code == 401
