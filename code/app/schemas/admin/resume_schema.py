import datetime
from typing import Optional
from uuid import UUID
from models.enums import ResumeStatusEnum
from schemas.base_schema import ABaseModel, BaseListResponseSchema, optional
from schemas.site.certificate_block_schema import ICertificateBlockReadSchema
from schemas.site.course_block_schema import ICourseBlockReadSchema
from schemas.site.education_block_schema import IEducationBlockReadSchema
from schemas.site.experience_block_schema import IExperienceBlockReadSchema
from schemas.site.language_block import ILanguageBlockReadSchema
from schemas.site.media_schema import IMediaShortReadSchema
from schemas.site.portfolio_link_block import IPortfolioLinkBlockReadSchema
from schemas.site.skill_block import ISkillBlockReadSchema
from schemas.site.social_link_block import ISocialLinkBlockReadSchema


class AResumeBaseSchema(ABaseModel):
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
    image: Optional[IMediaShortReadSchema]

    professional_summary: Optional[str]
    hobbies: Optional[str]
    educations: list[IEducationBlockReadSchema]
    experiences: list[IExperienceBlockReadSchema]
    certificates: list[ICertificateBlockReadSchema]
    social_links: list[ISocialLinkBlockReadSchema]
    portfolio_links: list[IPortfolioLinkBlockReadSchema]
    courses: list[ICourseBlockReadSchema]
    skills: list[ISkillBlockReadSchema]
    languages: list[ILanguageBlockReadSchema]

    is_active: bool
    is_verified: bool
    status: ResumeStatusEnum


class AResumeShortReadSchema(ABaseModel):
    id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    job_title: Optional[str]
    is_active: bool
    is_verified: bool
    status: ResumeStatusEnum


class AResumeReadSchema(AResumeBaseSchema):
    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


@optional
class AResumeUpdateSchema(AResumeBaseSchema):
    pass


class AListResponseSchema(BaseListResponseSchema):
    results: list[AResumeShortReadSchema]
