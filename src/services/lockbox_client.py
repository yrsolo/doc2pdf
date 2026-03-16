from __future__ import annotations

from typing import Any
import os

import httpx


LOCKBOX_DEFAULT_ENDPOINT = "https://payload.lockbox.api.cloud.yandex.net/lockbox/v1"
METADATA_TOKEN_URL = (
    "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
)


def load_lockbox_payload(lockbox_id: str) -> dict[str, str]:
    token = _get_iam_token()
    endpoint = os.getenv("LOCKBOX_ENDPOINT", LOCKBOX_DEFAULT_ENDPOINT).rstrip("/")
    url = f"{endpoint}/secrets/{lockbox_id}/payload"
    response = httpx.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=5.0,
    )
    response.raise_for_status()
    data = response.json()
    return _extract_payload_entries(data)


def _get_iam_token() -> str:
    token = os.getenv("LOCKBOX_IAM_TOKEN")
    if token:
        return token

    response = httpx.get(
        METADATA_TOKEN_URL,
        headers={"Metadata-Flavor": "Google"},
        timeout=2.0,
    )
    response.raise_for_status()
    payload = response.json()
    access_token = payload.get("access_token")
    if not access_token:
        raise RuntimeError("Lockbox token response did not include access_token.")
    return access_token


def _extract_payload_entries(data: dict[str, Any]) -> dict[str, str]:
    payload: dict[str, str] = {}
    for entry in data.get("entries", []):
        key = entry.get("key")
        if not key:
            continue
        if "text_value" in entry:
            payload[key] = entry["text_value"]
    return payload
