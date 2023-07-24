from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class IResumeReadSchema(BaseModel):
    id: UUID
    job_title: Optional[str]
    country: Optional[str]
    city: Optional[str]
    address: Optional[str]
    zipcode: Optional[str]
    nationality: Optional[str]
    driving_license: Optional[str]
    place_of_residence: Optional[str]
    date_of_birth: Optional[str]
    image_id: Optional[UUID]

    professional_summary = db.Column(db.Text)
    hobbies = db.Column(db.String)

    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)