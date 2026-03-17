from pathlib import Path

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse

from src.config import settings
from src.schemas import (
    ConversionRequest,
    ConversionResponse,
    HealthResponse,
    MvpConvertRequest,
    MvpPrepareUploadRequest,
    MvpPrepareUploadResponse,
    MvpUploadResponse,
)
from src.services.conversion_service import ConversionService
from src.services.gotenberg_client import GotenbergClient
from src.services.mvp_service import MvpService
from src.services.mvp_token_service import MvpTokenService
from src.services.object_storage_service import ObjectStorageService

router = APIRouter()
service = ConversionService(
    gotenberg_client=GotenbergClient(base_url=settings.gotenberg_base_url)
)
static_dir = Path(__file__).resolve().parent.parent / "static"

def require_token(x_shared_token: str | None = Header(default=None)) -> None:
    if not settings.shared_token:
        return
    if x_shared_token is None:
        raise HTTPException(status_code=401, detail="missing X-Shared-Token")
    if x_shared_token != settings.shared_token:
        raise HTTPException(status_code=401, detail="invalid X-Shared-Token")


def build_mvp_service() -> MvpService:
    return MvpService(
        conversion_service=service,
        object_storage_service=ObjectStorageService(),
        token_service=MvpTokenService(),
    )

@router.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    return HealthResponse(status="ok", gotenberg_base_url=settings.gotenberg_base_url)


@router.get("/", include_in_schema=False)
async def index() -> FileResponse:
    return FileResponse(static_dir / "mvp.html")


@router.get("/api-help", include_in_schema=False)
async def api_help() -> FileResponse:
    return FileResponse(static_dir / "api-help.html")


@router.post("/convert/doc-to-pdf", response_model=ConversionResponse, dependencies=[Depends(require_token)])
async def convert_doc_to_pdf(request: ConversionRequest) -> ConversionResponse:
    return await service.convert_doc_to_pdf(request)


@router.post("/mvp/prepare-upload", response_model=MvpPrepareUploadResponse, include_in_schema=False)
async def mvp_prepare_upload(request: MvpPrepareUploadRequest) -> MvpPrepareUploadResponse:
    if not request.filename.strip():
        raise HTTPException(status_code=400, detail="filename is required")

    try:
        mvp_service = build_mvp_service()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return mvp_service.prepare_upload(
        filename=request.filename,
        content_type=request.content_type,
    )


@router.post("/mvp/convert", response_model=MvpUploadResponse, include_in_schema=False)
async def mvp_convert(request: MvpConvertRequest) -> MvpUploadResponse:
    if not request.conversion_token.strip():
        raise HTTPException(status_code=400, detail="conversion_token is required")

    try:
        mvp_service = build_mvp_service()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    try:
        return await mvp_service.convert_prepared_upload(request.conversion_token)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/mvp/upload", response_model=MvpUploadResponse, include_in_schema=False)
async def mvp_upload(file: UploadFile = File(...)) -> MvpUploadResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="filename is required")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="empty file")

    try:
        mvp_service = build_mvp_service()
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return await mvp_service.convert_uploaded_file(
        filename=file.filename,
        content=content,
    )
