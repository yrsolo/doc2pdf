# DTM Gotenberg Converter

Separate microservice repository for legacy `.doc` / `.docx` -> PDF preview conversion for DTM attachments.

## Purpose
This repo contains an independently deployable converter carrier so the main DTM backend does not need to be redeployed whenever preview-conversion logic changes.

## Initial design
- runtime: Yandex Serverless Container
- engine: Gotenberg (`gotenberg/gotenberg:8`) as the primary conversion carrier
- integration style: backend orchestrates conversion jobs and passes presigned Object Storage URLs
- output: PDF preview artifact written back to Object Storage
- ownership: this repo owns only conversion concerns, not DTM task/domain logic

## Recommended flow
1. DTM backend detects legacy `.doc` or unsupported-in-browser office document.
2. Backend creates presigned GET URL for source object and presigned PUT URL for target PDF preview.
3. Backend calls converter API `/convert/doc-to-pdf`.
4. Converter instructs Gotenberg to fetch the source via presigned GET and upload result via presigned PUT.
5. Backend updates `preview_state` / `derived_preview_ref`.

## Repo map
- `config/` - tracked non-secret configuration and templates.
- `src/` - tiny wrapper service around Gotenberg.
- `docs/` - architecture and interface docs.
- `work/` - process and campaign tracking, same style as DTM backend repo.
- `.github/workflows/` - image build and deploy workflows.
- `deploy/` - deployment examples and environment templates.

## Configuration split
- `config/` contains non-secret settings and checked-in templates.
- `.env` is for local secrets and machine-specific overrides only.

## Local Proof Workflow
The public API stays aligned with the future backend integration shape. For early carrier proof on a real legacy file, use a dev-only smoke script instead of adding a temporary multipart endpoint.

Local proof inputs:
- `example/example.doc` is a temporary local sample only
- it is not treated as a permanent CI fixture
- it should later be replaced by a safe anonymized fixture or by a documented local sample drop-in flow

Local proof steps:
1. Start Gotenberg locally with `docker compose up gotenberg`.
2. Run `python scripts/smoke_local_conversion.py --input example/example.doc`.
3. Review the generated PDF under `example/output/`.
4. Review the captured evidence under `work/roadmap/campaigns/CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1/evidence/`.

This smoke flow is for local engine validation only. It does not define the service's stable API.

## MVP
The current skeleton is intentionally thin:
- a small FastAPI wrapper;
- a Gotenberg-backed conversion adapter;
- health endpoint;
- conversion endpoint contract;
- CI skeleton for image build and Yandex Serverless Container deployment.

## Non-goals for MVP
- multi-format rendering UI;
- auth facade for external browsers;
- preview status persistence;
- conversion queueing;
- retries/orchestration;
- direct Object Storage event triggers.

Those remain owned by DTM backend/orchestrator.
