import sqlalchemy as db
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates, relationship, backref
from sqlalchemy_utils import URLType

from core.babel_config import _
from exceptions import CustomValidationError
from utils.uuid6 import uuid7
from .base_model import BaseModel, base_validate_level, base_validate_positive
from .enums import ResumeStatusEnum


class Sphere(BaseModel):
    """
    class Sphere
        - Программирование
        - Инжинерия
        - Уборка
    """
    is_active = db.Column(db.Boolean, default=True, server_default=db.true())
    professions = relationship('Profession', backref='sphere', cascade="all,delete")
    translations = relationship('SphereTranslation', backref='translation', cascade="all,delete")


class SphereTranslation(BaseModel):
    sphere_id = db.Column(db.Integer, db.ForeignKey("sphere.id", ondelete="CASCADE"), index=True, nullable=False)
    title = db.Column(db.String, nullable=False, index=True)
    description = db.Column(db.String)
    language_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('sphere_id', 'language_id'),
    )

    @validates('language_id')
    def validate_language_id(self, key, value):
        return base_validate_positive(key, value)


class Profession(BaseModel):
    """
    class Profession
        - Программист
        - Инженер по компьютерам
        - Уборщик по домам
    """
    sphere_id = db.Column(db.Integer, db.ForeignKey("sphere.id", ondelete="CASCADE"), index=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("profession.id", ondelete="CASCADE"), index=True)
    is_default = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True, server_default=db.true())

    sub_professions = relationship('Profession', backref=backref('parent', remote_side='Profession.id'),
                                   cascade="all,delete")
    translations = relationship('ProfessionTranslation', backref='translation', cascade="all,delete")

    __table_args__ = (
        db.Index('only_one_active_is_default', is_default,
                 unique=True,
                 postgresql_where=is_default),
    )


class ProfessionTranslation(BaseModel):
    profession_id = db.Column(db.Integer, db.ForeignKey("profession.id", ondelete="CASCADE"), index=True, nullable=False)
    title = db.Column(db.String, nullable=False, index=True)
    description = db.Column(db.String)
    language_id = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('profession_id', 'language_id'),
    )

    @validates('language_id')
    def validate_language_id(self, key, value):
        return base_validate_positive(key, value)


class Resume(BaseModel):
    id = db.Column(UUID, primary_key=True, default=uuid7)
    user_id = db.Column(UUID)
    profession_id = db.Column(db.Integer, db.ForeignKey("profession.id", ondelete="CASCADE"), index=True, nullable=False)

    first_name = db.Column(db.String, index=True)
    last_name = db.Column(db.String, index=True)
    email = db.Column(db.String, index=True)
    phone = db.Column(db.String, index=True)
    job_title = db.Column(db.String, index=True)
    country = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    zipcode = db.Column(db.String)
    nationality = db.Column(db.String)
    driving_license = db.Column(db.String)
    place_of_residence = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    image_id = db.Column(UUID, db.ForeignKey('media.id', ondelete="CASCADE"))
    template_id = db.Column(db.Integer)

    professional_summary = db.Column(db.Text)
    hobbies = db.Column(db.String)

    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    status = db.Column(Enum(ResumeStatusEnum), default=ResumeStatusEnum.DRAFT, nullable=False)

    educations = relationship('EducationBlock', backref='resume', cascade="all,delete")
    experiences = relationship('ExperienceBlock', backref='resume', cascade="all,delete")
    certificates = relationship('CertificateBlock', backref='resume', cascade="all,delete")
    social_links = relationship('SocialLinkBlock', backref='resume', cascade="all,delete")
    portfolio_links = relationship('PortfolioLinkBlock', backref='resume', cascade="all,delete")
    courses = relationship('CourseBlock', backref='resume', cascade="all,delete")
    skills = relationship('SkillBlock', backref='resume', cascade="all,delete")
    languages = relationship('LanguageBlock', backref='resume', cascade="all,delete")
    image = relationship("Media", foreign_keys=[image_id], backref="resume", cascade="all,delete")
    profession = relationship("Profession", foreign_keys=[profession_id], backref=backref("resume", cascade="all,delete"))


class ResumeBaseBlock(BaseModel):
    __abstract__ = True

    id = db.Column(UUID, primary_key=True, default=uuid7)
    page = db.Column(db.Integer, default=1)

    @declared_attr
    def resume_id(cls):
        return db.Column(UUID, db.ForeignKey("resume.id", ondelete="CASCADE"), nullable=False)

    @declared_attr
    def __table_args__(cls):
        db.CheckConstraint("0 < cls.page AND cls.page <= 10", name='check_page'), {}

    @validates('page')
    def validate_page(self, key, value):
        if not 0 < value <= 10:
            raise CustomValidationError(_("Percent should be greater 0, equal or smaller 10"))
        return value


class SocialLinkBlock(ResumeBaseBlock):
    title = db.Column(db.String)
    url = db.Column(URLType)
    description = db.Column(db.String)


class PortfolioLinkBlock(ResumeBaseBlock):
    title = db.Column(db.String)
    url = db.Column(URLType)
    description = db.Column(db.String)


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


class SkillBlock(ResumeBaseBlock):
    name = db.Column(db.String)
    level = db.Column(db.Integer, default=10)

    @validates('level')
    def validate_level(self, key, value):
        return base_validate_level(key, value)


class LanguageBlock(ResumeBaseBlock):
    name = db.Column(db.String)
    level = db.Column(db.Integer, default=10)

    @validates('level')
    def validate_level(self, key, value):
        return base_validate_level(key, value)


class CourseBlock(ResumeBaseBlock):
    name = db.Column(db.String)
    organization_title = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)


class CertificateBlock(ResumeBaseBlock):
    name = db.Column(db.String)
    file_id = db.Column(UUID, db.ForeignKey('media.id', ondelete="CASCADE"))

    file = relationship("Media", foreign_keys=[file_id], backref="certificate", cascade="all,delete")

# @event.listens_for(CertificateBlock, 'after_delete')
# def check_email_and_phone(mapper, connection, target):
#     import crud
#     from utils.deps import minio_auth
#     if target.file_id:
#         obj = crud.media.get(where={Media.id: target.file_id})
#         minio_client = minio_auth()
#         minio_client.remove_object(obj.path)
