# Interfaces

## Internal caller
Trusted DTM backend or internal worker only.

## Auth
MVP uses a simple shared token via `X-Shared-Token`.
This can later be replaced by IAM/private ingress policy.

## HTTP API

### GET /healthz
Returns converter liveness information.

Response example:
```json
{
  "status": "ok",
  "gotenberg_base_url": "http://gotenberg:3000"
}
```

### POST /convert/doc-to-pdf
Converts a legacy office document to PDF preview.

Request body:
```json
{
  "attachment_id": "att_123",
  "source_url": "https://storage-presigned-get.example",
  "target_url": "https://storage-presigned-put.example",
  "source_filename": "legacy.doc",
  "target_filename": "preview.pdf",
  "request_id": "req-001"
}
```

Response body:
```json
{
  "status": "ready",
  "attachment_id": "att_123",
  "preview_mime": "application/pdf",
  "preview_size_bytes": 123456,
  "error_code": null,
  "error_message": null
}
```
