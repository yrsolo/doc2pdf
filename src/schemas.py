from typing import Literal, Optional
from pydantic import BaseModel, HttpUrl

class ConversionRequest(BaseModel):
    attachment_id: str
    source_url: HttpUrl
    target_url: HttpUrl
    source_filename: str
    target_filename: str = "preview.pdf"
    request_id: Optional[str] = None

class ConversionResponse(BaseModel):
    status: Literal["ready", "failed"]
    attachment_id: str
    preview_mime: str = "application/pdf"
    preview_size_bytes: Optional[int] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    gotenberg_base_url: str


class MvpUploadResponse(BaseModel):
    status: Literal["ready", "failed"]
    attachment_id: str
    filename: str
    preview_url: Optional[HttpUrl] = None
    preview_size_bytes: Optional[int] = None
    source_object_key: Optional[str] = None
    preview_object_key: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class MvpPrepareUploadRequest(BaseModel):
    filename: str
    content_type: Optional[str] = None


class MvpPrepareUploadResponse(BaseModel):
    status: Literal["prepared"]
    filename: str
    source_object_key: str
    preview_object_key: str
    upload_url: HttpUrl
    upload_method: Literal["PUT"] = "PUT"
    upload_headers: dict[str, str]
    preview_url: HttpUrl
    conversion_token: str


class MvpConvertRequest(BaseModel):
    conversion_token: str
