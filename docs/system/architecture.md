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
4. converter delegates to Gotenberg
5. converter returns `ready|failed`
6. backend persists preview result

## Why separate repo
- independent Docker image lifecycle
- no need to redeploy main backend for converter changes
- easier runtime experimentation
- easier replacement of Gotenberg later if needed
