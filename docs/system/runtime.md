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

## Deployment assumptions
- image is stored in Yandex Container Registry
- service is exposed only to trusted internal callers
- DTM backend owns presigned Object Storage URLs
