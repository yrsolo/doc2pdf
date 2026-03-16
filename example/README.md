# Example

`example/example.doc` is a temporary local smoke sample.

Generated PDFs from the local smoke script are written to `example/output/`.
Those generated files are ignored by git.

`example/test-client.html` is a standalone browser test page.
Open it directly from disk and point it at a running doc2pdf service base URL, for example `http://localhost:8080`.

The page uses the cloud-safe hosted-upload flow:
1. `POST /mvp/prepare-upload`
2. direct PUT to Object Storage
3. `POST /mvp/convert`
4. open the returned `preview_url`
