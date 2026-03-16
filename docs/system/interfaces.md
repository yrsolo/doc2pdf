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

## Browser-facing MVP helper
The repo additionally exposes a browser-facing helper flow for manual testing from inside or outside the service origin.
It is not the public integration contract for DTM backend, but it is useful for smoke checks and external verification.

### POST /mvp/prepare-upload
Creates a hosted-upload session for a browser client.

Request body:
```json
{
  "filename": "legacy.doc",
  "content_type": "application/msword"
}
```

Response body:
```json
{
  "status": "prepared",
  "filename": "legacy.doc",
  "source_object_key": "doc2pdf/uploads/abc-legacy.doc",
  "preview_object_key": "doc2pdf/previews/def-legacy.pdf",
  "upload_url": "https://storage-presigned-put.example",
  "upload_method": "PUT",
  "upload_headers": {
    "Content-Type": "application/msword",
    "Content-Disposition": "attachment; filename=\"legacy.doc\""
  },
  "preview_url": "https://storage-presigned-get.example",
  "conversion_token": "opaque-short-lived-token"
}
```

### POST /mvp/convert
Finalizes a hosted-upload conversion after the browser has uploaded the source directly to Object Storage.

Request body:
```json
{
  "conversion_token": "opaque-short-lived-token"
}
```

Response body:
Same as `MvpUploadResponse`, including `preview_url` when conversion succeeds.

### POST /mvp/upload
Legacy multipart helper kept for local/dev convenience only.

Do not use this as the primary cloud path because large uploads can hit Serverless Container request-size limits.
