from typing import Optional, Annotated, Any

from pydantic import AnyHttpUrl, AnyUrl, AfterValidator, field_validator

from schemas.base_schema import IBaseModel


class ISocialLinkBlockReadSchema(IBaseModel):
    title: str | None = None
    url: Annotated[AnyUrl | None, AfterValidator(lambda v: str(v)), None]
    description: Optional[str] = None
    page: int

    # @field_validator("url")
    # def change_url_to_str(cls, v: AnyUrl) -> str:
    #     return str(v)
