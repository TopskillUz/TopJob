from schemas.base_schema import IBaseModel, BaseListResponseSchema
from schemas.site.profession_schema import IProfessionReadSchema


class ISphereTranslation(IBaseModel):
    title: str
    description: str | None = None
    language_id: int


class ISphereReadSchema(IBaseModel):
    id: int
    translations: list[ISphereTranslation]
    professions: list[IProfessionReadSchema]


class IListResponseSchema(BaseListResponseSchema):
    results: list[ISphereReadSchema]
