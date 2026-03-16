from src.schemas import ConversionRequest, ConversionResponse

class GotenbergClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    async def convert_doc_to_pdf(self, request: ConversionRequest) -> ConversionResponse:
        # Skeleton only.
        # Production implementation should use a Gotenberg zero-transfer pipeline:
        # 1. ask Gotenberg to fetch source_url
        # 2. convert via LibreOffice route
        # 3. upload result to target_url
        return ConversionResponse(
            status="failed",
            attachment_id=request.attachment_id,
            error_code="not_implemented",
            error_message="Gotenberg zero-transfer conversion pipeline is not implemented in this skeleton.",
        )
