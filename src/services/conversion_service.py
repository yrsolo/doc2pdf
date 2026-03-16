from src.schemas import ConversionRequest, ConversionResponse
from src.services.gotenberg_client import GotenbergClient


class ConversionService:
    def __init__(self, gotenberg_client: GotenbergClient) -> None:
        self.gotenberg_client = gotenberg_client

    async def convert_doc_to_pdf(self, request: ConversionRequest) -> ConversionResponse:
        return await self.gotenberg_client.convert_doc_to_pdf(request)
