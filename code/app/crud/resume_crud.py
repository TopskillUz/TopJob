from io import BytesIO

from fastapi import UploadFile
from fastapi_sqlalchemy import db
from sqlalchemy.orm import RelationshipProperty
from starlette.responses import Response

from core.config import settings
from models import Media, Resume
from utils.minio_client import MinioClient
from utils.modify_media import check_file_ext, modify_image, get_filename_and_extension
from utils.uuid6 import uuid7
from .base_crud import BaseCrud, SchemaType, ModelType


class ResumeCrud(BaseCrud):
    @classmethod
    def update_fields(cls, resume: Resume, payload: SchemaType):
        data = payload.model_dump(exclude_none=True)
        for key, value in data.items():
            instrumented_attr = getattr(Resume, key)
            if isinstance(instrumented_attr.property, RelationshipProperty):
                rel_class = instrumented_attr.property.mapper.class_
                attr = getattr(resume, key)
                for item in attr:
                    db.session.delete(item)
                updated_data = [rel_class(**data) for data in value]
            else:
                updated_data = value
            setattr(resume, key, updated_data)

            db.session.add(resume)
            db.session.commit()
        db.session.refresh(resume)
        return resume

    def update_image(self, obj: ModelType, image: UploadFile | None, minio_client: MinioClient):
        if not image:
            media_id = getattr(obj, 'image_id', None)

            if media_id:
                from . import media
                # update
                media_obj = media.get(where={Media.id: media_id})
                # remove old image from minio
                if media_obj:
                    minio_client.remove_object(media_obj.path)
                    db.session.delete(media_obj)
                    db.session.commit()
            return Response(status_code=204)

        check_file_ext(image, settings.SUPPORTED_IMAGE_TYPES)
        image_data = modify_image(image=image)
        old_filename, file_ext = get_filename_and_extension(image.filename)
        filename = f"{old_filename}{file_ext}"
        file_path = f"resumes/user-images/{uuid7()}{file_ext}"

        self.upsert_media(
            obj=obj,
            filename=filename,
            file_path=file_path,
            field_name="image_id",
            file_data=image_data,
            content_type=image.content_type,
            size=image.size,
            minio_client=minio_client)
        db.session.refresh(obj)
        return obj.image


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
