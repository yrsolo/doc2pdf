from fastapi.testclient import TestClient

from src.api import routes
from src.main import app


def test_root_serves_mvp_page():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert "doc2pdf test client" in response.text


def test_mvp_prepare_upload_returns_upload_session(monkeypatch):
    client = TestClient(app)

    class FakeMvpService:
        def prepare_upload(self, filename: str, content_type: str | None = None):
            return {
                "status": "prepared",
                "filename": filename,
                "source_object_key": "doc2pdf/uploads/source.doc",
                "preview_object_key": "doc2pdf/previews/source.pdf",
                "upload_url": "https://storage.example/upload",
                "upload_method": "PUT",
                "upload_headers": {"Content-Type": content_type or "application/msword"},
                "preview_url": "https://storage.example/preview.pdf",
                "conversion_token": "opaque-token",
            }

    monkeypatch.setattr(routes, "build_mvp_service", lambda: FakeMvpService())

    response = client.post(
        "/mvp/prepare-upload",
        json={"filename": "example.doc", "content_type": "application/msword"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "prepared"
    assert body["upload_url"] == "https://storage.example/upload"
    assert body["conversion_token"] == "opaque-token"


def test_mvp_convert_returns_preview_url(monkeypatch):
    client = TestClient(app)

    class FakeMvpService:
        async def convert_prepared_upload(self, conversion_token: str):
            return {
                "status": "ready",
                "attachment_id": "mvp-test",
                "filename": "example.doc",
                "preview_url": "https://storage.example/preview.pdf",
                "preview_size_bytes": 12345,
                "source_object_key": "doc2pdf/uploads/source.doc",
                "preview_object_key": "doc2pdf/previews/source.pdf",
                "error_code": None,
                "error_message": None,
            }

    monkeypatch.setattr(routes, "build_mvp_service", lambda: FakeMvpService())

    response = client.post(
        "/mvp/convert",
        json={"conversion_token": "opaque-token"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["preview_url"] == "https://storage.example/preview.pdf"


def test_mvp_upload_returns_preview_url(monkeypatch):
    client = TestClient(app)

    class FakeMvpService:
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

    monkeypatch.setattr(routes, "build_mvp_service", lambda: FakeMvpService())

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
