from core.config import settings
from utils.modify_media import check_file_ext, modify_image, get_filename_and_extension
from utils.uuid6 import uuid7
from .base_crud import BaseCrud


class ResumeCrud(BaseCrud):
    def save_image(self, obj, image, minio_client):
        check_file_ext(image, settings.SUPPORTED_IMAGE_TYPES)
        image_data = modify_image(image=image)
        old_filename, file_ext = get_filename_and_extension(image.filename)
        filename = f"{old_filename}{file_ext}"
        self.upsert_media(
            obj=obj,
            filename=filename,
            file_path=f"resumes/user-images/{filename}",
            field_name="image_id",
            file_data=image_data,
            content_type=image.content_type,
            size=image.size,
            minio_client=minio_client)
