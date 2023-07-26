import datetime
from typing import Optional

from schemas.base_schema import IBaseModel


class ICourseBlockReadSchema(IBaseModel):
    name: str
    organization_title: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    page: int
