from pathlib import Path

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse

from src.config import settings
from src.schemas import (
    ConversionRequest,
    ConversionResponse,
    HealthResponse,
    MvpUploadResponse,
)
from src.services.conversion_service import ConversionService
from src.services.gotenberg_client import GotenbergClient
from src.services.mvp_service import MvpService
from src.services.object_storage_service import ObjectStorageService

router = APIRouter()
service = ConversionService(
    gotenberg_client=GotenbergClient(base_url=settings.gotenberg_base_url)
)
static_dir = Path(__file__).resolve().parent.parent / "static"

def require_token(x_shared_token: str | None = Header(default=None)) -> None:
    if settings.shared_token and x_shared_token != settings.shared_token:
        raise HTTPException(status_code=401, detail="unauthorized")

@router.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    return HealthResponse(status="ok", gotenberg_base_url=settings.gotenberg_base_url)


@router.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(static_dir / "mvp.html")


@router.post("/convert/doc-to-pdf", response_model=ConversionResponse, dependencies=[Depends(require_token)])
async def convert_doc_to_pdf(request: ConversionRequest) -> ConversionResponse:
    return await service.convert_doc_to_pdf(request)


@router.post("/mvp/upload", response_model=MvpUploadResponse, include_in_schema=False)
async def mvp_upload(file: UploadFile = File(...)) -> MvpUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="filename is required")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="empty file")

    try:
        mvp_service = MvpService(
            conversion_service=service,
            object_storage_service=ObjectStorageService(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return await mvp_service.convert_uploaded_file(
        filename=file.filename,
        content=content,
    )
