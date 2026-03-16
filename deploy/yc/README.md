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
- `DOC2PDF_AWS_ACCESS_KEY_ID`
- `DOC2PDF_AWS_SECRET_ACCESS_KEY`
- `DOC2PDF_OBJECT_STORAGE_BUCKET`
- `DOC2PDF_OBJECT_STORAGE_PREFIX`
- `DOC2PDF_OBJECT_STORAGE_ENDPOINT`
- `DOC2PDF_OBJECT_STORAGE_REGION`
- `DOC2PDF_OBJECT_STORAGE_PRESIGN_TTL_SEC`

## Deployment shape
1. Build image.
2. Push image to Yandex Container Registry.
3. Deploy the same single image that runs both wrapper and Gotenberg.
4. Set env vars:
   - `PORT=8080`
   - `GOTENBERG_BASE_URL=http://127.0.0.1:3000`
   - `SHARED_TOKEN`
   - Object Storage credentials and bucket settings

## Cloud endpoint shape
- Serverless Container URL: `https://<your-container-id>.containers.yandexcloud.net/`

## External browser MVP prerequisites
- The container must allow unauthenticated invoke, or be fronted by an ingress/auth layer that a browser client can use.
- Object Storage bucket CORS must allow browser `PUT` and `GET` from the origin used by the test page, including `Content-Type` and `Content-Disposition` headers.
- Browser uploads must use the hosted-upload flow:
  1. `POST /mvp/prepare-upload`
  2. direct PUT to Object Storage
  3. `POST /mvp/convert`

Do not rely on `POST /mvp/upload` in cloud for larger files, because Serverless Container ingress enforces request body limits.
