# Interfaces

## Internal caller
Trusted DTM backend or internal worker only.

## Auth
MVP uses a simple shared token via `X-Shared-Token`.
This can later be replaced by IAM/private ingress policy.

## Contract stability
This interface is the stable converter service contract for future backend integration.
Local smoke or proof-of-carrier tooling must not redefine this API as multipart upload or local-output semantics.

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

## Current implementation note
The stable request/response contract already matches the intended backend integration shape.

The current implementation path is:
1. Gotenberg downloads the source document from `source_url`
2. the wrapper receives the produced PDF
3. the wrapper uploads the PDF to `target_url`

This avoids introducing a temporary multipart upload contract while keeping the service narrow.

## Local MVP helper
The repo may additionally expose a local-only MVP helper flow for manual testing in a browser.
That helper may upload a local file to Object Storage and then call the stable conversion service internally, but it is not the public integration contract for DTM backend.
The helper is served from the same container runtime as the stable API.
