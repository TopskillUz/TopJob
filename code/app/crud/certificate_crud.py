from io import BytesIO

from fastapi import UploadFile
from fastapi_sqlalchemy import db

from core.config import settings
from utils.minio_client import MinioClient
from utils.modify_media import check_file_ext, get_filename_and_extension
from utils.uuid6 import uuid7
from .base_crud import BaseCrud, ModelType


class CertificateBlockCrud(BaseCrud):
    def update_file(self, obj: ModelType, file: UploadFile, minio_client: MinioClient):
        check_file_ext(file, settings.SUPPORTED_MEDIA_TYPES)
        old_filename, file_ext = get_filename_and_extension(file.filename)
        filename = f"{old_filename}{file_ext}"
        file_path = f"resumes/certificates/{uuid7()}{file_ext}"
        self.upsert_media(
            obj=obj,
            filename=filename,
            file_path=file_path,
            field_name="file_id",
            file_data=BytesIO(file.file.read()),
            content_type=file.content_type,
            size=file.size,
            minio_client=minio_client)
        db.session.refresh(obj)
        return obj.file