from typing import ForwardRef

from schemas.base_schema import IBaseModel, BaseListResponseSchema


class IProfessionTranslationSchema(IBaseModel):
    title: str
    description: str | None = None
    language_id: int


IProfessionReadSchema = ForwardRef('IProfessionReadSchema')


class IProfessionReadSchema(IBaseModel):
    id: int
    translations: list[IProfessionTranslationSchema]
    sphere_id: int
    sub_professions: list[IProfessionReadSchema]
    is_default: bool


class IListResponseSchema(BaseListResponseSchema):
    results: list[IProfessionReadSchema]
