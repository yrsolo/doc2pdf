# CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1

## Status
In Progress

## Owner
Converter service

## Goal
Stand up an independent microservice repository for DTM document preview conversion using Gotenberg as the primary engine.

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
- CI image build workflow
- Yandex Serverless Container deploy workflow
- system and interface docs
- process materials in `work/`

### Out
- backend lifecycle persistence
- frontend integration
- direct storage event triggers
- retries and queue ownership
- full production hardening

## Done when
1. Repo is structured and documented.
2. Local stack starts with wrapper + Gotenberg.
3. Health endpoint works.
4. Conversion endpoint contract is frozen.
5. Container build workflow exists.
6. Deploy workflow for Yandex Serverless Container exists.
