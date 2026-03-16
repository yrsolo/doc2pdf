# Runtime notes

## Primary carrier
Yandex Serverless Container.

## Why not Cloud Function
Legacy office conversion needs a containerized runtime and should stay independently deployable.

## External dependency
Gotenberg is the current conversion engine and is bundled into the same runtime image as the wrapper service.

## Current execution model
The wrapper currently performs a narrow two-step execution:
1. ask Gotenberg to fetch and convert the source document from `source_url`
2. upload the returned PDF to `target_url`

This keeps source transfer out of the wrapper while preserving the stable backend-facing API.

## Runtime shape
Local MVP and Serverless Container deployment use the same container shape:
- one image
- Gotenberg running on `127.0.0.1:3000`
- FastAPI wrapper running on `0.0.0.0:8080`
- Object Storage remains external

## Configuration
Required environment variables:
- `PORT`
- `GOTENBERG_BASE_URL`
- `SHARED_TOKEN`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `OBJECT_STORAGE_BUCKET`

Optional:
- `GOTENBERG_TIMEOUT_SEC`
- `OBJECT_STORAGE_ENDPOINT`
- `OBJECT_STORAGE_REGION`
- `OBJECT_STORAGE_PREFIX`
- `OBJECT_STORAGE_PRESIGN_TTL_SEC`

## Local proof tooling
The repo may include dev-only smoke tooling for local conversion proof against Gotenberg.
That tooling is not part of the stable HTTP API contract and must not be treated as an integration surface for DTM backend.
It should be run through the container runtime, not through a host Python setup.

Tracked non-secret defaults belong in `config/`.
Secrets and machine-specific overrides belong in local `.env` files.

## Deployment assumptions
- image is stored in Yandex Container Registry
- service is exposed only to trusted internal callers
- DTM backend owns presigned Object Storage URLs
