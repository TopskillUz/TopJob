import sqlalchemy as db
from sqlalchemy.dialects.postgresql import UUID

from utils.uuid6 import uuid7
from .base_model import BaseModel


class Media(BaseModel):
    id = db.Column(UUID, primary_key=True, default=uuid7)
    filename = db.Column(db.String, nullable=False, unique=True)
    path = db.Column(db.String, nullable=True)
    size = db.Column(db.Integer, nullable=True)
    file_format = db.Column(db.String, nullable=False)
    created_by_id = db.Column(UUID)
    is_active = db.Column(db.Boolean, default=True)
