import datetime

from schemas.base_schema import ABaseModel, BaseListResponseSchema, optional


class ASphereTranslation(ABaseModel):
    title: str
    description: str | None = None
    language_id: int


class ABaseSphereSchema(ABaseModel):
    is_active: bool = None
    translations: list[ASphereTranslation]


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
