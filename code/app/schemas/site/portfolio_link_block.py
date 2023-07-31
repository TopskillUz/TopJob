from typing import Optional, Annotated

from pydantic import AnyHttpUrl, AnyUrl, AfterValidator

from schemas.base_schema import IBaseModel


class IPortfolioLinkBlockReadSchema(IBaseModel):
    title: str | None = None
    url: Annotated[AnyUrl | None, AfterValidator(lambda v: str(v)), None]
    description: str | None = None
    page: int
