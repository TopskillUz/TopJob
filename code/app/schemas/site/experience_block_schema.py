import datetime
from typing import Optional

from schemas.base_schema import IBaseModel


class IExperienceBlockReadSchema(IBaseModel):
    organization_title: Optional[str]
    employer: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    city: Optional[str]
    description: Optional[str]
    page: int
