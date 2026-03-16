from fastapi.testclient import TestClient

from src.config import settings
from src.main import app


def test_convert_endpoint_uses_json_contract_and_placeholder_response():
    client = TestClient(app)
    original_token = settings.shared_token
    settings.shared_token = "test-shared-token"

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

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "failed"
    assert body["attachment_id"] == "att_123"
    assert body["error_code"] == "not_implemented"


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
