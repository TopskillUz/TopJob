import sqlalchemy as db
from sqlalchemy import event
from sqlalchemy.dialects.postgresql import UUID

from utils.uuid6 import uuid7
from .base_model import BaseModel


class Media(BaseModel):
    id = db.Column(UUID, primary_key=True, default=uuid7)
    filename = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=True, unique=True)
    size = db.Column(db.Integer, nullable=True)
    file_format = db.Column(db.String, nullable=False)
    created_by_id = db.Column(UUID)
    is_active = db.Column(db.Boolean, default=True)


@event.listens_for(Media, 'after_delete')
def after_delete_media(mapper, connection, target):
    from utils.deps import minio_auth
    if target.path:
        minio_client = minio_auth()
        minio_client.remove_object(target.path)
