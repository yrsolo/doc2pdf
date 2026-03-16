# CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1 Notes

## Current approach
Use a tiny wrapper service and an adjacent Gotenberg container for local development.

## First wave framing
This wave is a carrier proof wave, but the stable API should not drift toward a temporary multipart or local-output contract.

Keep two paths distinct:
- stable service API for future DTM integration
- dev-only smoke tooling for local real-file conversion proof

## Production direction
Either:
- call Gotenberg directly from the wrapper, or
- replace the wrapper with a thinner adapter if direct Gotenberg invocation becomes acceptable.

## Preferred integration
Backend owns:
- presigned source GET URL
- presigned target PUT URL
- preview metadata persistence

Converter owns:
- conversion execution
- engine errors normalization

## Local proof path
Use a dev-only script or smoke utility to submit a local `.doc` file to Gotenberg and capture result evidence.

Rules:
- do not describe this as the public API
- do not tie CI compatibility claims to a single local sample
- use `example/example.doc` only as a temporary local sample until a safe fixture or documented local drop-in flow replaces it

## Evidence expectations
For each real-file smoke run capture:
- source filename
- output path
- output size bytes
- success or failure
- error details if any
- obvious rendering caveats after human review

## Deploy proof
This wave must preserve independent deployability of the wrapper service.
It does not require proof that the full conversion runtime shape already works inside Yandex Serverless Container.

## Key constraint
Keep this repo narrow. Do not move DTM backend business logic here.
