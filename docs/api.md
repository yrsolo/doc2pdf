# API Reference

This document describes the HTTP interface exposed by `doc2pdf`.

## Base URL

Local:

```text
http://localhost:8080
```

Cloud:

```text
https://<your-container-id>.containers.yandexcloud.net
```

Built-in help page exposed by the running service:

```text
<base-url>/api-help
```

## Auth

### Stable backend contract
`POST /convert/doc-to-pdf` expects a shared token in the header:

```http
X-Shared-Token: <token>
```

### Browser-facing MVP helper endpoints
The `/mvp/*` routes are intended for manual testing and smoke checks.
They do not use `X-Shared-Token` in the current MVP.

## Endpoints

### GET /healthz
Checks service liveness.

Response:

```json
{
  "status": "ok",
  "gotenberg_base_url": "http://127.0.0.1:3000"
}
```

### POST /convert/doc-to-pdf
Stable backend-facing conversion endpoint for clients that already have storage.

Request body:

```json
{
  "attachment_id": "att_123",
  "source_url": "https://storage.example/source.doc",
  "target_url": "https://storage.example/preview.pdf",
  "source_filename": "legacy.doc",
  "target_filename": "preview.pdf",
  "request_id": "req-001"
}
```

Fields:

- `attachment_id` - caller-owned attachment reference.
- `source_url` - presigned GET URL for the source document.
- `target_url` - presigned PUT URL where the wrapper should upload the PDF.
- `source_filename` - original file name used for converter metadata.
- `target_filename` - desired output file name, default `preview.pdf`.
- `request_id` - optional correlation id.

Success response:

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

Failure response:

```json
{
  "status": "failed",
  "attachment_id": "att_123",
  "preview_mime": "application/pdf",
  "preview_size_bytes": null,
  "error_code": "upstream_http_error",
  "error_message": "POST http://127.0.0.1:3000/forms/libreoffice/convert returned 502: bad gateway"
}
```

Example:

```bash
curl -X POST http://localhost:8080/convert/doc-to-pdf \
  -H "Content-Type: application/json" \
  -H "X-Shared-Token: change-me" \
  -d '{
    "attachment_id": "att_123",
    "source_url": "https://storage.example/source.doc",
    "target_url": "https://storage.example/preview.pdf",
    "source_filename": "legacy.doc",
    "target_filename": "preview.pdf",
    "request_id": "req-001"
  }'
```

### POST /mvp/prepare-upload
Browser-facing hosted-upload preparation endpoint for clients without their own storage.

Request body:

```json
{
  "filename": "legacy.doc",
  "content_type": "application/msword"
}
```

Success response:

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

Meaning:

- `upload_url` - presigned PUT URL for direct browser upload to Object Storage.
- `upload_headers` - headers that must be sent with the PUT request.
- `preview_url` - future presigned GET URL for the resulting PDF.
- `conversion_token` - opaque short-lived token later sent to `/mvp/convert`.

### POST /mvp/convert
Finalizes hosted-upload conversion after the browser has already uploaded the source file to Object Storage.

Request body:

```json
{
  "conversion_token": "opaque-short-lived-token"
}
```

Success response:

```json
{
  "status": "ready",
  "attachment_id": "mvp-123",
  "filename": "legacy.doc",
  "preview_url": "https://storage-presigned-get.example",
  "preview_size_bytes": 123456,
  "source_object_key": "doc2pdf/uploads/abc-legacy.doc",
  "preview_object_key": "doc2pdf/previews/def-legacy.pdf",
  "error_code": null,
  "error_message": null
}
```

Failure response:

```json
{
  "status": "failed",
  "attachment_id": "mvp-123",
  "filename": "legacy.doc",
  "preview_url": null,
  "preview_size_bytes": null,
  "source_object_key": "doc2pdf/uploads/abc-legacy.doc",
  "preview_object_key": "doc2pdf/previews/def-legacy.pdf",
  "error_code": "network_error",
  "error_message": "Connection refused"
}
```

### POST /mvp/upload
Legacy multipart helper endpoint.

This route is still useful for local/dev convenience, but it is not the preferred cloud path because Serverless Container ingress has request size limits.

Request:
- `multipart/form-data`
- field name: `file`

Response:
- same shape as `/mvp/convert`

## Supported flows

### Flow A: client already has storage
1. Client creates presigned `source_url`.
2. Client creates presigned `target_url`.
3. Client calls `POST /convert/doc-to-pdf`.
4. Service returns `ready` or `failed`.

### Flow B: client does not have storage
1. Client calls `POST /mvp/prepare-upload`.
2. Client uploads the source document directly to the returned `upload_url`.
3. Client calls `POST /mvp/convert` with `conversion_token`.
4. Client opens `preview_url`.

## Error model

Stable and MVP conversion responses normalize failures into:

- `upstream_http_error`
- `network_error`
- `internal_error`

Validation and route-level errors may also return regular FastAPI HTTP errors such as:

- `400` for invalid client input
- `401` for missing or wrong `X-Shared-Token`
- `500` for missing Object Storage configuration

## Notes for browser clients

- Hosted upload is the preferred browser flow.
- Direct upload requires Object Storage CORS to allow browser `PUT` and `GET`.
- When testing from `example/test-client.html`, the page may be opened directly from disk and pointed at either local or cloud base URL.
