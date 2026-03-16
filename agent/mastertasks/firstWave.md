Ниже — готовые тексты `.md` файлов для **первой кампании** в новом репозитории конвертера. Кампания сфокусирована на **bootstrap/proof-of-carrier**, с локальным поднятием, smoke-тестами и первым деплоем в Yandex Serverless Container.

### `work/roadmap/campaigns/CAM-BOOTSTRAP-GOTENBERG-CARRIER/campaign.md`

```md
# CAM-BOOTSTRAP-GOTENBERG-CARRIER

## Status
Proposed

## Owner
Converter service

## Goal
Поднять и проверить отдельный converter carrier на базе Gotenberg как самостоятельный микросервис в отдельном репозитории.

Цель этой первой волны:
- локально поднять сервис и Gotenberg;
- получить working happy-path `.doc -> pdf`;
- зафиксировать минимальный HTTP API сервиса;
- добавить локальные smoke-тесты;
- собрать и задеплоить контейнерный сервис в Yandex Serverless Container;
- получить доказательство, что carrier жизнеспособен на реальных legacy `.doc`.

## Why
Сейчас главный риск не в интеграции с DTM backend, а в том, что нужно сначала подтвердить жизнеспособность выбранного conversion engine на реальных артефактах.

Без этого преждевременно:
- строить backend orchestration;
- делать preview lifecycle integration;
- проектировать retry/error semantics глубже;
- тратить время на продовую интеграцию.

Сначала нужно ответить на практический вопрос:
- Gotenberg + LibreOffice вообще конвертирует наши реальные legacy `.doc` файлы в приемлемый PDF или нет.

## Scope
### In scope
- локальный запуск Gotenberg;
- локальный запуск тонкого converter service;
- health endpoint;
- минимальный convert endpoint;
- локальная конверсия тестовых `.doc` файлов в PDF;
- базовый storage-agnostic workflow для локального режима;
- docker compose/dev workflow;
- container build;
- deploy workflow для Yandex Serverless Container;
- smoke test instructions;
- фиксация известных ограничений.

### Out of scope
- интеграция с DTM backend;
- queue/job orchestration;
- presigned URL production flow;
- auth between backend and converter;
- retry policy beyond simple local errors;
- preview lifecycle updates in DTM;
- full production hardening;
- metrics/observability beyond basic logs;
- font-pack hardening beyond minimum needed to prove viability.

## Product decision for this wave
This is a **carrier proof** wave, not a full feature-complete product wave.

Success means:
- converter service can be run locally;
- Gotenberg can convert at least some real `.doc` samples into PDF;
- container can be built and deployed independently;
- service contract is stable enough for the next integration wave.

## Architecture constraints
1. Converter service lives in its own repository.
2. Converter service is independently deployable from DTM backend.
3. Gotenberg is treated as the underlying conversion engine.
4. Thin wrapper service owns the public/internal API contract for future DTM integration.
5. Local mode must work without Yandex Cloud dependencies.
6. The first wave may use direct local file input/output for smoke validation.
7. The first wave should not depend on DTM backend codebase.

## User stories
### US-01 Local engineer smoke
Developer clones repo, starts local stack, sends a `.doc`, gets a `.pdf`, and verifies that conversion is real.

### US-02 Real document validation
Developer runs several real legacy `.doc` files through the service and captures outcomes.

### US-03 Container proof
Developer builds the service container and confirms it is deployable independently.

### US-04 Serverless carrier proof
Developer deploys the service to Yandex Serverless Container and verifies health endpoint plus a minimal conversion call.

## Service contract for bootstrap wave
### Health
- `GET /healthz`
- response: simple JSON with `ok=true`

### Convert
- `POST /convert/doc-to-pdf`
- input (bootstrap-local mode):
  - multipart file upload with one `.doc`/`.docx` file
- response:
  - PDF file stream or
  - JSON with produced file path/reference in local mode

For bootstrap wave the contract may remain simple and local-first.
The next wave may add storage/presigned URL based transport.

## Local run modes
### Mode A — pure local smoke
- app service + gotenberg in docker compose
- test file mounted or uploaded through API
- output PDF written to local temp/output path or returned directly

### Mode B — local integration-like smoke
- service calls Gotenberg through internal docker network
- user verifies result with curl or simple script

## Deliverables
1. Running local stack with Gotenberg.
2. Wrapper service with health endpoint.
3. Wrapper service with minimal convert endpoint.
4. Smoke test instructions.
5. Example test fixtures folder.
6. Build workflow.
7. Deploy workflow.
8. Notes on real `.doc` compatibility and caveats.

## Files expected to exist
### Repo/process
- `AGENTS.md`
- `work/now/campaign.md`
- `work/now/tasks.md`
- `work/roadmap/campaigns/CAM-BOOTSTRAP-GOTENBERG-CARRIER/*`

### Service
- `src/main.py`
- `src/api/routes.py`
- `src/services/gotenberg_client.py`
- `src/services/conversion_service.py`

### Dev/runtime
- `Dockerfile`
- `docker-compose.yml`
- `.env.example`

### Tests
- `tests/test_health.py`
- `tests/test_convert_smoke.py`
- `fixtures/` with sample files or instructions to place local real samples

### CI/CD
- `.github/workflows/build.yml`
- `.github/workflows/deploy_yc_container.yml`

## Acceptance criteria
1. Local stack starts successfully.
2. `GET /healthz` returns success.
3. At least one local `.doc` converts to PDF through the service.
4. At least one additional real sample is tested and result is recorded.
5. Build pipeline can build container image.
6. Deploy pipeline for Yandex Serverless Container exists.
7. Known limitations are documented.
8. Evidence of local smoke is captured.

## Known risks to validate
- some legacy `.doc` files may fail or render poorly;
- fonts/layout may differ;
- cold starts may be slow;
- default resource settings may be insufficient;
- multipart upload may not be the final production transport.

## Done when
- carrier is locally proven;
- carrier is deployable;
- real sample outcomes are documented;
- repo is ready for the next campaign: backend integration.
```

---

### `work/roadmap/campaigns/CAM-BOOTSTRAP-GOTENBERG-CARRIER/tasks.md`

```md
# CAM-BOOTSTRAP-GOTENBERG-CARRIER Tasks

## P01 — Repo bootstrap and process structure

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P01-T001
Проверить и выровнять process-root структуру репозитория.

Acceptance:
- `work/` structure is present
- current campaign is registered in `work/now/*`
- campaign files exist and are coherent

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P01-T002
Заполнить `AGENTS.md` базовыми инструкциями для агента.

Acceptance:
- repo purpose is documented
- local/dev/deploy expectations are documented
- campaign-first workflow is stated

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P01-T003
Описать bootstrap service contract and goals in docs.

Acceptance:
- health endpoint documented
- convert endpoint documented
- local-first nature of wave documented

## P02 — Local runtime bootstrap

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P02-T001
Поднять Gotenberg локально через `docker-compose`.

Acceptance:
- `docker compose up` starts gotenberg successfully
- service is reachable from wrapper service
- local docs explain how to verify readiness

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P02-T002
Реализовать minimal wrapper service.

Acceptance:
- wrapper service starts locally
- has health endpoint
- can call Gotenberg over local docker network

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P02-T003
Реализовать local convert flow.

Acceptance:
- service accepts local file upload
- sends file to Gotenberg conversion endpoint
- returns or stores resulting PDF
- handles basic conversion errors cleanly

## P03 — Local smoke testing

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P03-T001
Добавить smoke test instructions in README/docs.

Acceptance:
- exact commands are documented
- one happy-path curl example exists
- output inspection path is clear

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P03-T002
Прогнать service на минимум одном test fixture.

Acceptance:
- conversion succeeds locally
- evidence captured in notes or closeout draft

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P03-T003
Прогнать service на нескольких реальных `.doc` samples.

Acceptance:
- at least 2–3 real sample outcomes recorded
- failures are documented honestly
- rendering caveats are noted

## P04 — Build and containerization

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P04-T001
Подготовить Dockerfile for wrapper service.

Acceptance:
- image builds locally
- runtime command is defined
- local docs explain build/run

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P04-T002
Подготовить build workflow.

Acceptance:
- workflow can build image on push/manual run
- image tagging strategy documented
- registry target is configurable

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P04-T003
Подготовить environment/config handling.

Acceptance:
- `.env.example` exists
- gotenberg base URL configurable
- service port configurable
- local temp/output path configurable if needed

## P05 — Yandex deploy bootstrap

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P05-T001
Подготовить deploy workflow for Yandex Serverless Container.

Acceptance:
- workflow exists
- required secrets/env vars documented
- deployment target can be updated independently of DTM backend

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P05-T002
Зафиксировать recommended initial resource settings.

Acceptance:
- memory/cores/timeout/concurrency recommendations documented
- rationale briefly noted

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P05-T003
Проверить deployed service health endpoint.

Acceptance:
- deployed `/healthz` returns success
- evidence captured

## P06 — Tests and evidence

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P06-T001
Добавить automated test for health endpoint.

Acceptance:
- test runs locally
- test included in test suite

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P06-T002
Добавить lightweight convert smoke test.

Acceptance:
- test or scripted smoke exists
- failure mode is understandable
- test does not pretend broader coverage than it has

### CAM-BOOTSTRAP-GOTENBERG-CARRIER-P06-T003
Подготовить evidence pack / closeout draft.

Acceptance:
- local run proof recorded
- real sample results recorded
- deployment proof recorded
- known limitations recorded
```

---

### `work/roadmap/campaigns/CAM-BOOTSTRAP-GOTENBERG-CARRIER/notes.md`

````md
# CAM-BOOTSTRAP-GOTENBERG-CARRIER Notes

## Purpose of this wave
This wave is about proving the carrier.
It is not yet about full DTM integration.

The service may remain intentionally simple:
- health endpoint
- convert endpoint
- local smoke workflow
- deployable container

## Recommended local architecture
Two services in docker compose:
1. `gotenberg`
2. `converter-api`

`converter-api` talks to `gotenberg` over docker network.

## Recommended first endpoint contract
### GET /healthz
Response:
```json
{ "ok": true }
````

### POST /convert/doc-to-pdf

Bootstrap-local mode:

* multipart form with uploaded file
* optional flags for debug/output behavior

Possible return strategies:

1. return PDF bytes directly
2. write PDF to local output dir and return metadata JSON

For the first wave either is acceptable.
Prefer the simplest implementation that enables smoke testing.

## Suggested env vars

* `PORT`
* `GOTENBERG_BASE_URL`
* `OUTPUT_DIR`
* `LOG_LEVEL`

Optional:

* `TMP_DIR`

## Suggested docker compose services

### gotenberg

* official image `gotenberg/gotenberg:8`
* exposed locally for smoke/debug
* reachable from wrapper by service name

### converter-api

* local app container
* mounts fixtures/output dirs if needed
* depends on gotenberg

## Suggested local smoke commands

Examples to document in README:

### start stack

```bash
docker compose up --build
```

### health

```bash
curl http://localhost:8000/healthz
```

### convert

```bash
curl -X POST http://localhost:8000/convert/doc-to-pdf \
  -F "file=@fixtures/sample.doc" \
  --output out/sample.pdf
```

## Real sample validation

Need a human-run validation step on real legacy `.doc` files.

Record for each sample:

* filename
* success/failure
* output produced or not
* major rendering issues
* notes about fonts/layout

Do not overclaim compatibility.

## Recommended initial deployment settings

Suggested starting point for serverless container:

* memory: 2 GB
* cores: 1
* timeout: 60–120 sec
* concurrency: 1

These are starting points only and may need adjustment after real test runs.

## Known likely issues

* missing fonts / layout shifts
* some `.doc` files may fail conversion
* cold start overhead
* longer-than-expected conversion times
* temporary file handling quirks

## Non-goals for this wave

* no presigned GET/PUT flow yet
* no backend auth
* no queue orchestration
* no preview_state integration
* no derived artifact metadata writeback
* no production SLAs

## Recommended implementation order

1. make local compose stack run
2. implement `/healthz`
3. implement local file convert endpoint
4. verify one happy-path fixture
5. verify several real `.doc`
6. add tests
7. add build workflow
8. add deploy workflow
9. verify deployed health endpoint

````

---

### `work/now/campaign.md`

```md
# Current Campaign

## Active campaign
- `CAM-BOOTSTRAP-GOTENBERG-CARRIER`

## Goal
Bootstrap and prove a separate Gotenberg-based converter carrier:
- local run;
- local `.doc -> pdf` smoke;
- minimal wrapper API;
- independent build/deploy;
- first deploy to Yandex Serverless Container.

## Why now
Before integrating with DTM backend, we need proof that the chosen conversion engine works on real legacy `.doc` files.

## Scope for current wave
In:
- local compose stack
- health endpoint
- minimal convert endpoint
- local tests
- build workflow
- deploy workflow
- first carrier validation

Out:
- DTM backend integration
- storage/presigned flow
- queue lifecycle
- auth/hardening
- preview metadata writeback

## Success criteria
- local stack runs;
- health endpoint works;
- at least one `.doc` converts successfully;
- several real samples are tested;
- service is independently deployable.
````

---

### `work/now/tasks.md`

```md
# Current Tasks

## Active campaign
`CAM-BOOTSTRAP-GOTENBERG-CARRIER`

## Current priorities

### 1. Local stack
- [ ] Make `docker compose up --build` start both services
- [ ] Verify Gotenberg readiness locally
- [ ] Verify wrapper service can reach Gotenberg

### 2. Minimal service API
- [ ] Implement `GET /healthz`
- [ ] Implement `POST /convert/doc-to-pdf`
- [ ] Handle local file upload
- [ ] Return or store produced PDF

### 3. Local smoke
- [ ] Add README commands for local run
- [ ] Add at least one sample fixture test
- [ ] Run conversion on 2–3 real legacy `.doc`
- [ ] Record observed compatibility issues

### 4. Tests
- [ ] Add health endpoint test
- [ ] Add lightweight convert smoke test
- [ ] Ensure local test flow is documented

### 5. Build/deploy
- [ ] Add Dockerfile for wrapper service
- [ ] Add GitHub Actions build workflow
- [ ] Add Yandex Serverless Container deploy workflow
- [ ] Document required secrets and env vars

### 6. First deployed proof
- [ ] Deploy service independently
- [ ] Verify deployed `/healthz`
- [ ] Record deployment evidence and caveats

## Next checkpoint
Local happy-path conversion first, then real sample validation, then deploy proof.
```

Если хочешь, следующим сообщением я могу сразу написать ещё и **README.md для этого репозитория** с командами локального запуска и тестов.
