# CAM-2026-03-16-GOTENBERG-CONVERTER-MVP-V1 Notes

## Current approach
Use a tiny wrapper service and an adjacent Gotenberg container for local development.

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

## Key constraint
Keep this repo narrow. Do not move DTM backend business logic here.
