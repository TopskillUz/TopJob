import datetime
import re

import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base

from core.babel_config import _
from exceptions import CustomValidationError


def camel_to_snake_case(name: str) -> str:
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', name).lower()


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake_case(cls.__name__)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column('updated_at', db.DateTime, onupdate=datetime.datetime.utcnow)
    deleted_at = db.Column(db.DateTime, default=None)


# Base = declarative_base()
BaseModel = declarative_base(cls=BaseModel)


# event.listen(async_engine, "handle_error", handler)
# @db.event.listens_for(db.orm.Mapper, 'refresh', named=True)
# def on_instance_refresh(target: type,
#                         context: db.orm.query.QueryContext,
#                         attrs: Optional[Set[str]]):
#     ssn: sqlalchemy.orm.Session = context.session
#     # target.deleted_at = datetime.datetime.now
#     print(38, target.id, attrs)
#     return target

def base_validate_not_negative(key, value):
    if value < 0:
        raise CustomValidationError(_('Value should not be negative'))
    return value


def base_validate_positive(key, value):
    if value <= 0:
        raise CustomValidationError(_('Value should be positive'))
    return value


def base_validate_level(key, value):
    if value % 10:
        raise CustomValidationError(_('Must be divisible by 10 without a remainder'))
    if not (0 < value <= 100):
        raise CustomValidationError(_('Value must be between 0 and 100'))
    return value

# https://stackoverflow.com/questions/27211361/sqlalchemy-declarative-inheritance-of-table-args
# https://stackoverflow.com/questions/63760639/sqlalchemy-checkconstraint-with-multiple-conditions-raises-warning
# https://stackoverflow.com/questions/20199462/sqlalchemy-postgresql-pg-regex
