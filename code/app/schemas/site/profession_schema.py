from typing import ForwardRef

from schemas.base_schema import IBaseModel


class IProfessionTranslationSchema(IBaseModel):
    title: str
    description: str | None = None
    language_id: int


IProfessionReadSchema = ForwardRef('IProfessionReadSchema')


class IProfessionReadSchema(IBaseModel):
    id: int
    translations: list[IProfessionTranslationSchema]
    sphere_id: int
    parent: IProfessionReadSchema | None
