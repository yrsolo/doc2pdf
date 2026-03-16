import time

from src.services.mvp_token_service import MvpTokenService


def test_mvp_token_round_trip(monkeypatch):
    monkeypatch.setattr("src.services.mvp_token_service.settings.shared_token", "test-shared-token")
    service = MvpTokenService()

    token = service.issue({"attachment_id": "mvp-123", "filename": "example.doc"})
    payload = service.verify(token)

    assert payload["attachment_id"] == "mvp-123"
    assert payload["filename"] == "example.doc"
    assert "exp" in payload


def test_mvp_token_rejects_expired_token(monkeypatch):
    monkeypatch.setattr("src.services.mvp_token_service.settings.shared_token", "test-shared-token")
    service = MvpTokenService()
    now = int(time.time())
    monkeypatch.setattr("src.services.mvp_token_service.time.time", lambda: now)
    token = service.issue({"attachment_id": "mvp-123"})
    monkeypatch.setattr("src.services.mvp_token_service.time.time", lambda: now + 7200)

    try:
        service.verify(token)
    except ValueError as exc:
        assert "expired" in str(exc)
    else:  # pragma: no cover - explicit failure path
        raise AssertionError("expired token must be rejected")
