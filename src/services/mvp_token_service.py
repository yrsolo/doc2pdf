from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time

from src.config import settings


class MvpTokenService:
    def __init__(self) -> None:
        secret = settings.shared_token or settings.aws_secret_access_key
        if not secret:
            raise ValueError("MVP token signing secret is not configured.")

        self.secret = secret.encode("utf-8")
        self.ttl_sec = settings.mvp_token_ttl_sec

    def issue(self, payload: dict[str, object]) -> str:
        token_payload = dict(payload)
        token_payload["exp"] = int(time.time()) + self.ttl_sec
        raw = json.dumps(token_payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        signature = hmac.new(self.secret, raw, hashlib.sha256).digest()
        return f"{self._encode(raw)}.{self._encode(signature)}"

    def verify(self, token: str) -> dict[str, object]:
        try:
            raw_part, signature_part = token.split(".", 1)
        except ValueError as exc:
            raise ValueError("Invalid conversion token format.") from exc

        raw = self._decode(raw_part)
        provided_signature = self._decode(signature_part)
        expected_signature = hmac.new(self.secret, raw, hashlib.sha256).digest()
        if not hmac.compare_digest(provided_signature, expected_signature):
            raise ValueError("Invalid conversion token signature.")

        payload = json.loads(raw.decode("utf-8"))
        if int(payload.get("exp", 0)) < int(time.time()):
            raise ValueError("Conversion token expired.")
        return payload

    @staticmethod
    def _encode(value: bytes) -> str:
        return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")

    @staticmethod
    def _decode(value: str) -> bytes:
        padding = "=" * (-len(value) % 4)
        return base64.urlsafe_b64decode(value + padding)
