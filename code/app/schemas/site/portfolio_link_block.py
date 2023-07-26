from typing import Optional

from pydantic import AnyHttpUrl

from schemas.base_schema import IBaseModel


class IPortfolioLinkBlockReadSchema(IBaseModel):
    title: str
    url: AnyHttpUrl
    description: Optional[str]
    page: int
