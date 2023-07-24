import enum

import sqlalchemy as db

from utils.uuid6 import uuid7
from .base_model import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import URLType
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Enum


class Resume(BaseModel):
    id = db.Column(UUID, primary_key=True, default=uuid7)
    user_id = db.Column(UUID)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    job_title = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    zipcode = db.Column(db.String)
    nationality = db.Column(db.String)
    driving_license = db.Column(db.String)
    place_of_residence = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    image_id = db.Column(UUID, db.ForeignKey('media.id', ondelete="CASCADE"))

    professional_summary = db.Column(db.Text)
    hobbies = db.Column(db.String)

    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)


class ResumeBaseBlock(BaseModel):
    __abstract__ = True

    @declared_attr
    def resume_id(cls):
        return db.Column(UUID, db.ForeignKey("resume.id"), nullable=False)


class SocialLinkBlock(ResumeBaseBlock):
    title = db.Column(db.String)
    url = db.Column(URLType)


class PortfolioLinkBlock(ResumeBaseBlock):
    title = db.Column(db.String)
    url = db.Column(URLType)


class EducationBlock(ResumeBaseBlock):
    organization_title = db.Column(db.String)
    degree = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    city = db.Column(db.String)
    description = db.Column(db.String)


class ExperienceBlock(ResumeBaseBlock):
    job_title = db.Column(db.String)
    employer = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    city = db.Column(db.String)
    description = db.Column(db.String)


class SkillLevelEnum(str, enum.Enum):
    NOVICE = "novice"
    BEGINNER = "beginner"
    SKILLFUL = "skillful"
    EXPERIENCED = "experienced"
    EXPERT = "expert"


class SkillBlock(ResumeBaseBlock):
    name = db.Column(db.String)
    level = db.Column(Enum(SkillLevelEnum), default=SkillLevelEnum.NOVICE)


class LanguageLevelEnum(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    PROFICIENT = "proficient"
    FLUENT = "fluent"
    NATIVE = "native"


class LanguageBlock(ResumeBaseBlock):
    name = db.Column(db.String)
    level = db.Column(Enum(LanguageLevelEnum), default=LanguageLevelEnum.BEGINNER)


class CourseBlock(ResumeBaseBlock):
    name = db.Column(db.String)
    organization_title = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
