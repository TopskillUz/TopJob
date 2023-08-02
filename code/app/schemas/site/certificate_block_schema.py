from typing import Optional
from uuid import UUID

from schemas.base_schema import IBaseModel
from schemas.site.media_schema import IMediaShortReadSchema


class ICertificateBlockCreateSchema(IBaseModel):
    name: str
    page: int


class ICertificateBlockReadSchema(ICertificateBlockCreateSchema):
    id: UUID
    file: Optional[IMediaShortReadSchema]
