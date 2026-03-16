from fastapi import APIRouter, Depends, Header, HTTPException
from src.config import settings
from src.schemas import ConversionRequest, ConversionResponse, HealthResponse
from src.services.gotenberg_client import GotenbergClient

router = APIRouter()
client = GotenbergClient(base_url=settings.gotenberg_base_url)

def require_token(x_shared_token: str | None = Header(default=None)) -> None:
    if settings.shared_token and x_shared_token != settings.shared_token:
        raise HTTPException(status_code=401, detail="unauthorized")

@router.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    return HealthResponse(status="ok", gotenberg_base_url=settings.gotenberg_base_url)

@router.post("/convert/doc-to-pdf", response_model=ConversionResponse, dependencies=[Depends(require_token)])
async def convert_doc_to_pdf(request: ConversionRequest) -> ConversionResponse:
    return await client.convert_doc_to_pdf(request)
