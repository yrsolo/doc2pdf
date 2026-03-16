# CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1 Tasks

## P01 — Repo skeleton
### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P01-T001
Create repository structure and base docs.

### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P01-T002
Add `AGENTS.md`, `work/*`, and system docs.

## P02 — HTTP service skeleton
### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P02-T001
Add FastAPI app and `/healthz`.

### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P02-T002
Add `/convert/doc-to-pdf` contract and placeholder implementation.

## P03 — Containerization
### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P03-T001
Add Dockerfile for wrapper service.

### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P03-T002
Add local docker-compose with Gotenberg.

## P04 — CI / Deploy
### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P04-T001
Add GitHub Actions workflow for image build and push.

### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P04-T002
Add manual deploy workflow for Yandex Serverless Container revision.

## P05 — Integration docs
### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P05-T001
Document backend -> converter API contract.

### CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1-P05-T002
Document runtime assumptions and env vars.
