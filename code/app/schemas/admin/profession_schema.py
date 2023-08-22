import datetime
from typing import ForwardRef

from schemas.base_schema import ABaseModel, BaseListResponseSchema, optional


class AProfessionTranslationSchema(ABaseModel):
    title: str
    description: str | None = None


class ABaseProfessionSchema(ABaseModel):
    is_default: bool
    is_active: bool = None
    translations: list[AProfessionTranslationSchema]
    sphere_id: int


AProfessionReadSchema = ForwardRef('AProfessionReadSchema')


class AProfessionReadSchema(ABaseProfessionSchema):
    id: int
    parent: AProfessionReadSchema | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


AProfessionReadSchema.model_rebuild()


class AProfessionCreateSchema(ABaseProfessionSchema):
    is_default: bool | None = False
    parent_id: int | None = None


@optional
class AProfessionUpdateSchema(ABaseProfessionSchema):
    is_default: bool | None
    parent_id: int | None


class AListResponseSchema(BaseListResponseSchema):
    results: list[AProfessionReadSchema]
