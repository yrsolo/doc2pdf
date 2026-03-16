# AGENTS.md

## Project intent
This repository hosts a narrow utility service: office document preview conversion for DTM attachments.

The main goal is to keep conversion runtime and its binary dependencies isolated from the main DTM backend repository.

## Working style
- Keep entrypoints thin.
- Keep conversion-specific logic inside `src/services/`.
- Keep process materials in `work/`.
- Keep system/runtime/integration docs in `docs/`.
- Prefer explicit contracts over hidden coupling to DTM backend internals.
- Treat Object Storage and converter APIs as external boundaries.

## Rules
1. Do not add DTM business logic here.
2. Do not reimplement attachment lifecycle orchestration that belongs to DTM backend.
3. Keep HTTP API narrow and stable.
4. Prefer configuration over hardcoded environment-specific constants.
5. Changes to deployment or runtime assumptions must be reflected in `docs/system/`.
6. Campaign state changes must update `work/now/campaign.md` first.

## Primary responsibilities
- accept conversion requests from trusted backend callers;
- invoke Gotenberg safely;
- return normalized result contracts;
- expose health/readiness diagnostics;
- remain independently deployable.

## Out of scope
- frontend concerns;
- end-user auth;
- long-term preview metadata persistence;
- DTM task read model changes;
- upload/download UI logic.

## Delivery process
Follow the same lightweight campaign flow as backend:
- active state in `work/now/`
- planned campaigns in `work/roadmap/campaigns/`
- completed campaigns in `work/archive/campaigns/`

## Implementation preference
Start thin:
- FastAPI wrapper
- Gotenberg HTTP integration
- presigned URL pipeline
- deterministic JSON response contracts
