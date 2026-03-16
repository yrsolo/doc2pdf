# First Wave Reframe: Carrier Proof Without API Drift

## Intent
The first wave remains a proof-of-carrier wave, but it must not introduce a temporary public API that we will later discard.

The stable service contract stays aligned with the future DTM integration model:
- `GET /healthz` returns the current documented JSON payload
- `POST /convert/doc-to-pdf` keeps the backend-style JSON contract with presigned `source_url` / `target_url`

To prove the conversion engine on real legacy `.doc` files, we add a separate local smoke/evidence path that is explicitly dev-only and does not redefine the service API.

## Goals
- prove that Gotenberg can convert real legacy `.doc` files locally
- keep the wrapper service contract stable while the conversion implementation is still incomplete
- separate local proof of conversion from future backend integration semantics
- keep deployment proof and local conversion proof as distinct outcomes

## Non-goals
- no temporary multipart upload public endpoint
- no local-output public API contract
- no attachment lifecycle logic from DTM backend
- no retry/queue orchestration
- no promise of full serverless conversion execution in this wave

## Campaign alignment
This wave is a sub-phase of the active campaign:
- `CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1`

Do not create a competing bootstrap campaign. Update the active campaign materials instead.

## Required outcomes
1. The repository and process materials describe one stable direction only.
2. The public API stays aligned with the presigned URL contract.
3. Local smoke tooling proves real-file conversion without changing the public API.
4. Evidence capture exists for local real-file conversion results.
5. Deployment materials continue to prove independent deployability of the carrier wrapper.

## Implementation guidance

### 1. Stable API remains stable
- keep `docs/system/interfaces.md` as the source of truth for the service API
- keep `src/services/gotenberg_client.py` oriented toward the zero-transfer production path
- do not add multipart upload handling to `POST /convert/doc-to-pdf`

### 2. Add a dev-only smoke path
Preferred approach:
- add a local script or smoke utility that submits a real `.doc` file directly to Gotenberg for proof-of-conversion
- record output metadata and caveats for manual review

Allowed fallback:
- add a dev-only helper endpoint only if a script is not sufficient

Constraints:
- the smoke path must be clearly documented as non-stable
- it must not be described as the service's public contract
- it may depend on local Docker Compose networking

### 3. Use the current sample conservatively
`example/example.doc` may be used for early local smoke only.

Rules:
- do not treat it as a permanent CI fixture
- do not build long-term compatibility claims on this single file
- document that it should later be replaced by an anonymized safe fixture or by instructions for local sample injection

### 4. Distinguish proof types
Local proof:
- Gotenberg converts a real `.doc` locally
- evidence is captured

Deploy proof:
- wrapper image builds and deploy workflow remains valid
- deployed health endpoint is enough for this wave unless serverless conversion runtime is explicitly proven

## Evidence expectations
For each local smoke run, capture:
- source filename
- output path
- output size in bytes
- success or failure
- error details if any
- obvious rendering caveats after manual review

Store the evidence in campaign materials, not in ad hoc chat history.

## Documentation expectations
The docs for this wave must make the distinction explicit:
- stable service API
- local smoke/proof workflow
- temporary status of `example/example.doc`
- config policy: tracked non-secret config in `config/`, secrets only in `.env`

## Acceptance criteria
1. `GET /healthz` still matches the documented response shape.
2. `POST /convert/doc-to-pdf` still uses the documented JSON contract.
3. A local smoke workflow exists for `example/example.doc`.
4. Smoke results can be recorded with file size, outcome, and caveats.
5. Campaign/work docs refer to one active campaign and one terminology set.
6. Build/deploy materials remain valid for an independently deployable carrier.

## Suggested deliverables
- updated campaign/work docs
- updated README section for local proof workflow
- dev-only smoke script
- evidence template for real-file conversion outcomes
- automated tests that guard against API drift toward multipart/local-only behavior

## Assumptions
- `example/example.doc` is temporary and local-use only for now
- deployment proof and conversion proof are intentionally separate in this wave
- auth and presigned transport remain part of the intended final architecture even if the conversion engine proof is still being gathered
