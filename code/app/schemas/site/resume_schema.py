import datetime
from uuid import UUID

from models import ResumeStatusEnum
from schemas.base_schema import IBaseModel, BaseListResponseSchema
from schemas.site.certificate_block_schema import ICertificateBlockReadSchema
from schemas.site.course_block_schema import ICourseBlockReadSchema
from schemas.site.education_block_schema import IEducationBlockReadSchema
from schemas.site.experience_block_schema import IExperienceBlockReadSchema
from schemas.site.language_block import ILanguageBlockReadSchema
from schemas.site.media_schema import IMediaShortReadSchema
from schemas.site.portfolio_link_block import IPortfolioLinkBlockReadSchema
from schemas.site.skill_block_schema import ISkillBlockReadSchema
from schemas.site.social_link_block import ISocialLinkBlockReadSchema


class IResumeReadSchema(IBaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None
    email: str | None
    phone: str | None
    job_title: str | None
    country: str | None
    city: str | None
    address: str | None
    zipcode: str | None
    nationality: str | None
    driving_license: str | None
    place_of_residence: str | None
    date_of_birth: datetime.date | None
    image: IMediaShortReadSchema | None
    status: ResumeStatusEnum
    template_id: UUID | None

    professional_summary: str | None
    hobbies: str | None
    educations: list[IEducationBlockReadSchema]
    experiences: list[IExperienceBlockReadSchema]
    certificates: list[ICertificateBlockReadSchema]
    social_links: list[ISocialLinkBlockReadSchema]
    portfolio_links: list[IPortfolioLinkBlockReadSchema]
    courses: list[ICourseBlockReadSchema]
    skills: list[ISkillBlockReadSchema]
    languages: list[ILanguageBlockReadSchema]


class IResumeUpdateSchema(IBaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    job_title: str | None = None
    country: str | None = None
    city: str | None = None
    address: str | None = None
    zipcode: str | None = None
    nationality: str | None = None
    driving_license: str | None = None
    place_of_residence: str | None = None
    date_of_birth: datetime.date | None = None
    status: ResumeStatusEnum = None
    template_id: UUID | None

    professional_summary: str | None = None
    hobbies: str | None = None
    educations: list[IEducationBlockReadSchema] = None
    experiences: list[IExperienceBlockReadSchema] = None
    social_links: list[ISocialLinkBlockReadSchema] = None
    portfolio_links: list[IPortfolioLinkBlockReadSchema] = None
    courses: list[ICourseBlockReadSchema] = None
    skills: list[ISkillBlockReadSchema] = None
    languages: list[ILanguageBlockReadSchema] = None


class IListResponseSchema(BaseListResponseSchema):
    results: list[IResumeReadSchema]
