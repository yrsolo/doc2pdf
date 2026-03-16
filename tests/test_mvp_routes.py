from fastapi.testclient import TestClient

from src.api import routes
from src.main import app


def test_root_serves_mvp_page():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "doc2pdf test client" in response.text


def test_mvp_upload_returns_preview_url(monkeypatch):
    client = TestClient(app)

    class FakeObjectStorageService:
        pass

    class FakeMvpService:
        def __init__(self, conversion_service, object_storage_service):
            self.conversion_service = conversion_service
            self.object_storage_service = object_storage_service

        async def convert_uploaded_file(self, filename: str, content: bytes):
            return {
                "status": "ready",
                "attachment_id": "mvp-test",
                "filename": filename,
                "preview_url": "https://example.com/preview.pdf",
                "preview_size_bytes": len(content),
                "source_object_key": "doc2pdf/uploads/source.doc",
                "preview_object_key": "doc2pdf/previews/source.pdf",
                "error_code": None,
                "error_message": None,
            }

    monkeypatch.setattr(routes, "ObjectStorageService", FakeObjectStorageService)
    monkeypatch.setattr(routes, "MvpService", FakeMvpService)

    response = client.post(
        "/mvp/upload",
        files={
            "file": (
                "example.doc",
                b"fake-doc-content",
                "application/msword",
            )
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["preview_url"] == "https://example.com/preview.pdf"
    assert body["filename"] == "example.doc"
