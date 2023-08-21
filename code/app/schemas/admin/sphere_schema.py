import datetime

from schemas.base_schema import ABaseModel, BaseListResponseSchema, optional


class ABaseSphereSchema(ABaseModel):
    title: str
    description: str | None
    is_active: bool = None


class ASphereReadSchema(ABaseSphereSchema):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class ASphereCreateSchema(ABaseSphereSchema):
    pass


@optional
class ASphereUpdateSchema(ABaseSphereSchema):
    pass


class AListResponseSchema(BaseListResponseSchema):
    results: list[ASphereReadSchema]
