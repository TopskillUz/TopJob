from uuid import UUID

from schemas.base_schema import IBaseModel


class IBaseMediaSchema(IBaseModel):
    filename: str
    path: str
    size: int
    file_format: str


class IMediaCreateSchema(IBaseMediaSchema):
    pass


class IMediaReadSchema(IBaseMediaSchema):
    id: UUID


class IMediaShortReadSchema(IBaseModel):
    filename: str
    path: str
