# Architecture

## Purpose
This service is a narrow converter carrier used by DTM backend for attachment preview generation.

## Core values
- separate deploy cadence from main DTM backend;
- isolate heavy/binary conversion concerns;
- keep a tiny HTTP API;
- treat DTM backend as the orchestrator;
- return deterministic machine-readable conversion results.

## Contours
### Converter service
Owns:
- conversion request intake
- Gotenberg integration
- health/readiness endpoint
- normalized result contract

### DTM backend
Owns:
- attachment lifecycle
- preview queueing / retries
- preview metadata persistence
- auth to end-user preview routes
- read model publication

## Conversion model
Preferred production flow:
1. backend generates presigned GET for source
2. backend generates presigned PUT for target PDF
3. backend calls `/convert/doc-to-pdf`
4. converter asks the co-located Gotenberg runtime to fetch and convert the source
5. converter uploads the resulting PDF to target storage
6. converter returns `ready|failed`
7. backend persists preview result

Hosted-upload helper flow for browser-based testing:
1. browser requests `/mvp/prepare-upload`
2. converter returns a presigned source upload URL and opaque conversion token
3. browser uploads the source directly to Object Storage
4. browser calls `/mvp/convert`
5. converter recreates internal source/target URLs and runs the same conversion pipeline

## Runtime packaging
The wrapper and Gotenberg are packaged into the same container image so the local Docker runtime and Yandex Serverless Container use the same deployment shape.

## Why separate repo
- independent Docker image lifecycle
- no need to redeploy main backend for converter changes
- easier runtime experimentation
- easier replacement of Gotenberg later if needed
