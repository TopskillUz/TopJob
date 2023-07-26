from typing import Optional
from uuid import UUID

from schemas.base_schema import IBaseModel
from schemas.site.course_block_schema import ICourseBlockReadSchema
from schemas.site.education_block_schema import IEducationBlockReadSchema
from schemas.site.experience_block_schema import IExperienceBlockReadSchema
from schemas.site.portfolio_link_block import IPortfolioLinkBlockReadSchema
from schemas.site.skill_block import ISkillBlockReadSchema
from schemas.site.social_link_block import ISocialLinkBlockReadSchema


class IResumeReadSchema(IBaseModel):
    id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
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

    professional_summary: Optional[str]
    hobbies: Optional[str]
    educations: list[IEducationBlockReadSchema]
    experiences: list[IExperienceBlockReadSchema]
    social_links: list[ISocialLinkBlockReadSchema]
    portfolio_links: list[IPortfolioLinkBlockReadSchema]
    courses: list[ICourseBlockReadSchema]
    skills: list[ISkillBlockReadSchema]
    languages: list[ISkillBlockReadSchema]


class IResumeUpdateSchema(IBaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    zipcode: Optional[str] = None
    nationality: Optional[str] = None
    driving_license: Optional[str] = None
    place_of_residence: Optional[str] = None
    date_of_birth: Optional[str] = None
    image_id: Optional[UUID] = None

    professional_summary: Optional[str] = None
    hobbies: Optional[str] = None
    educations: list[IEducationBlockReadSchema] = None
    experiences: list[IExperienceBlockReadSchema] = None
    social_links: list[ISocialLinkBlockReadSchema] = None
    portfolio_links: list[IPortfolioLinkBlockReadSchema] = None
    courses: list[ICourseBlockReadSchema] = None
    skills: list[ISkillBlockReadSchema] = None
    languages: list[ISkillBlockReadSchema] = None
