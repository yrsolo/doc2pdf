# DTM Gotenberg Converter

Separate microservice repository for legacy `.doc` / `.docx` -> PDF preview conversion for DTM attachments.

## Purpose
This repo contains an independently deployable converter carrier so the main DTM backend does not need to be redeployed whenever preview-conversion logic changes.

## Initial design
- runtime: Yandex Serverless Container
- engine: Gotenberg (`gotenberg/gotenberg:8`) bundled into the same runtime image as the wrapper
- integration style: backend orchestrates conversion jobs and passes presigned Object Storage URLs
- output: PDF preview artifact written back to Object Storage
- ownership: this repo owns only conversion concerns, not DTM task/domain logic

## Recommended flow
1. DTM backend detects legacy `.doc` or unsupported-in-browser office document.
2. Backend creates presigned GET URL for source object and presigned PUT URL for target PDF preview.
3. Backend calls converter API `/convert/doc-to-pdf`.
4. Converter instructs Gotenberg to fetch the source via presigned GET and upload result via presigned PUT.
5. Backend updates `preview_state` / `derived_preview_ref`.

## Supported client modes

### Bring your own storage
Use the stable backend-facing contract:
- caller provides `source_url`
- caller provides `target_url`
- caller calls `POST /convert/doc-to-pdf`

This is the intended DTM integration path.

### Hosted upload
Use the browser-facing MVP flow when the client does not own storage:
1. call `POST /mvp/prepare-upload`
2. upload the source document directly to Object Storage via the returned presigned PUT URL
3. call `POST /mvp/convert` with the returned opaque conversion token
4. open the returned `preview_url`

This avoids Serverless Container request body limits because the file bypasses the container during upload.

## Repo map
- `config/` - tracked non-secret configuration and templates.
- `src/` - tiny wrapper service around Gotenberg.
- `docs/` - architecture and interface docs.
- `work/` - process and campaign tracking, same style as DTM backend repo.
- `.github/workflows/` - image build and deploy workflows.
- `deploy/` - deployment examples and environment templates.

## Documentation

- [Docs index](./docs/README.md)
- [API reference](./docs/api.md)
- [Repository guide](./docs/repository.md)
- [System architecture](./docs/system/architecture.md)
- [Runtime notes](./docs/system/runtime.md)

Built-in runtime docs:
- `/api-help` - lightweight HTML reference served by the app itself
- `/docs` - Swagger UI generated from OpenAPI
- `/redoc` - ReDoc generated from OpenAPI

## Configuration split
- `config/` contains non-secret settings and checked-in templates.
- `.env` is for local secrets and machine-specific overrides only.

## Local MVP Client
The local developer flow is container-only. No local Python runtime is required.

The MVP flow is intentionally separate from the stable backend-facing API:
1. the browser requests `POST /mvp/prepare-upload`
2. the wrapper returns a presigned source upload URL plus an opaque conversion token
3. the browser uploads the source directly to Yandex Object Storage
4. the browser calls `POST /mvp/convert`
5. the wrapper generates internal source/target URLs, converts via Gotenberg, and uploads the PDF
6. the page opens the resulting PDF in an embedded preview frame

Required local configuration for the MVP page:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `OBJECT_STORAGE_BUCKET`
- optional `OBJECT_STORAGE_PREFIX`
- optional `OBJECT_STORAGE_ENDPOINT`
- optional `OBJECT_STORAGE_REGION`

Run locally:
1. `docker compose up --build`
2. open `http://localhost:8080/`
3. upload `example/example.doc` or another `.doc/.docx`
4. verify that the embedded preview opens the resulting PDF from Object Storage

External browser test page:
- open `example/test-client.html` directly from disk
- set the service base URL, for example `http://localhost:8080`
- run the same direct-to-storage flow from outside the service origin
- when testing against cloud, ensure the Object Storage bucket allows browser `PUT`/`GET` via CORS

Diagnostics:
- `docker compose logs -f app`

Optional containerized smoke helper:
- `docker compose exec app python scripts/smoke_local_conversion.py --input example/example.doc`

## MVP
The current MVP stays intentionally thin:
- a small FastAPI wrapper;
- a Gotenberg-backed conversion adapter inside the same container image;
- health endpoint;
- conversion endpoint contract;
- CI skeleton for image build and Yandex Serverless Container deployment.

Current conversion path:
1. Gotenberg fetches the source document from the presigned `source_url`.
2. The wrapper receives the produced PDF from Gotenberg.
3. The wrapper uploads the PDF to the presigned `target_url`.

This keeps the stable API shape while avoiding a temporary multipart upload contract.

## Non-goals for MVP
- multi-format rendering UI;
- auth facade for external browsers;
- preview status persistence;
- conversion queueing;
- retries/orchestration;
- direct Object Storage event triggers.

Those remain owned by DTM backend/orchestrator.
