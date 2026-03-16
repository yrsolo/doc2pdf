# CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1

## Status
In Progress

## Owner
Converter service

## Goal
Stand up an independent microservice repository for DTM document preview conversion using Gotenberg as the primary engine, while proving real legacy `.doc` conversion without drifting away from the intended service API.

## Why
Legacy `.doc` preview conversion should be isolated from the main DTM backend:
- separate deploy cadence
- separate binary/runtime concerns
- minimal contract between orchestrator and converter

## Scope
### In
- separate repository skeleton
- tiny FastAPI wrapper
- health endpoint
- conversion endpoint contract
- Dockerfile
- local docker-compose with Gotenberg
- dev-only local smoke tooling for real-file conversion proof
- evidence capture for real `.doc` outcomes
- CI image build workflow
- Yandex Serverless Container deploy workflow
- system and interface docs
- process materials in `work/`

### Out
- backend lifecycle persistence
- frontend integration
- direct storage event triggers
- retries and queue ownership
- temporary multipart/local-first public API
- full production hardening

## Done when
1. Repo is structured and documented.
2. Local stack starts with wrapper + Gotenberg.
3. Health endpoint works.
4. Conversion endpoint contract is frozen.
5. Local smoke workflow proves at least one real `.doc` conversion path without changing the public API.
6. Real-file evidence is captured with outcome and caveats.
7. Container build workflow exists.
8. Deploy workflow for Yandex Serverless Container exists.
