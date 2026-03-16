# Yandex deployment notes

## Required resources
- Container Registry
- Serverless Container
- Service account / IAM permissions
- Secret or CI variables for registry auth and deployment identifiers

## Expected GitHub secrets
- `YC_SA_JSON_CREDENTIALS`
- `YC_REGISTRY_ID`
- `YC_FOLDER_ID`
- `YC_DOC_CONVERTER_CONTAINER_ID`
- `YC_DOC_CONVERTER_IMAGE_NAME`
- `DOC_CONVERTER_SHARED_TOKEN`

## Deployment shape
1. Build image.
2. Push image to Yandex Container Registry.
3. Deploy new Serverless Container revision.
4. Set env vars:
   - `PORT=8080`
   - `GOTENBERG_BASE_URL`
   - `SHARED_TOKEN`
