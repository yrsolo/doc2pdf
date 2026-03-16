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
