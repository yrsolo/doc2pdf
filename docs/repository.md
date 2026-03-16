# Repository Guide

This page explains what this repository contains and where to look for things.

## What this repo is

`doc2pdf` is a narrow utility service for converting office documents into PDF previews.

It exists to keep heavy conversion runtime and binary dependencies outside the main DTM backend repository.

## What this repo is not

This repo does not own:

- DTM attachment lifecycle
- preview persistence
- queueing and retries
- end-user authentication
- frontend product UI

## Directory map

### src/
Application code.

- `src/main.py` - FastAPI app bootstrap.
- `src/api/` - thin HTTP routes.
- `src/services/` - conversion, storage, token, and MVP orchestration logic.
- `src/static/` - built-in test page served from `/`.

### docs/
Repository and system documentation.

- `docs/api.md` - endpoint reference.
- `docs/repository.md` - this guide.
- `docs/system/` - architecture, interfaces, runtime assumptions.

### config/
Tracked non-secret configuration templates.

Use this for checked-in defaults and examples.

### deploy/
Deployment notes and environment templates.

### example/
Manual test assets.

- `example/example.doc` - temporary smoke sample.
- `example/test-client.html` - standalone browser test client.

### work/
Campaign and delivery tracking in the same style as the backend repo.

## Main runtime shape

- one container image
- Gotenberg inside the same image
- FastAPI wrapper inside the same image
- Object Storage as an external boundary
- Yandex Serverless Container as the primary deployment target

## Main integration modes

### Stable backend mode
For DTM backend or another trusted caller:

- use `POST /convert/doc-to-pdf`
- pass presigned `source_url` and `target_url`

### Browser test mode
For manual testing and smoke checks:

- use `POST /mvp/prepare-upload`
- upload directly to Object Storage
- use `POST /mvp/convert`

## Local development

Primary local path:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8080/
```

Or open:

```text
example/test-client.html
```

and point it to the service base URL.

## Documentation map

If you want to understand the repo quickly:

1. read [API Reference](./api.md)
2. read [System Architecture](./system/architecture.md)
3. read [Runtime Notes](./system/runtime.md)
