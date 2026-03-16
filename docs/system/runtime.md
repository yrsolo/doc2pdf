# Runtime notes

## Primary carrier
Yandex Serverless Container.

## Why not Cloud Function
Legacy office conversion needs a containerized runtime and should stay independently deployable.

## External dependency
Gotenberg is the current conversion engine.

## Configuration
Required environment variables:
- `PORT`
- `GOTENBERG_BASE_URL`
- `SHARED_TOKEN`

Optional:
- `GOTENBERG_TIMEOUT_SEC`

## Local proof tooling
The repo may include dev-only smoke tooling for local conversion proof against Gotenberg.
That tooling is not part of the stable HTTP API contract and must not be treated as an integration surface for DTM backend.

Tracked non-secret defaults belong in `config/`.
Secrets and machine-specific overrides belong in local `.env` files.

## Deployment assumptions
- image is stored in Yandex Container Registry
- service is exposed only to trusted internal callers
- DTM backend owns presigned Object Storage URLs
