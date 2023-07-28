import os
from io import BytesIO
from typing import Optional

from PIL import Image
from fastapi import UploadFile
from core.babel_config import _
from exceptions import CustomValidationError


def modify_image(image: UploadFile, width: Optional[int] = None, height: Optional[int] = None) -> BytesIO:
    img = Image.open(BytesIO(image.file.read()))
    if not width:
        width = img.width
    if not height:
        height = img.height
    image = img.resize((width, height), Image.LANCZOS)
    output = BytesIO()
    image.save(output, format=img.format, optimize=True, quality=100)
    return BytesIO(output.getvalue())


def modify_file(file: UploadFile) -> BytesIO:
    file = BytesIO(file.file.read())
    return file


def get_filename_and_extension(filename: str) -> tuple[str, str]:
    filename, file_ext = os.path.splitext(filename)
    return filename, file_ext


def check_file_ext(file: UploadFile, supported_types: dict) -> UploadFile:
    if file.content_type not in supported_types:
        raise CustomValidationError(_(
            "{content_type} file type is not allowed! Allowed file types {supported_types}").format(
            content_type=file.content_type, supported_types=list(supported_types.keys())))
    filename, file_ext = get_filename_and_extension(file.filename)
    # # video/mpeg formatda bir nechta kengaytmalar bo'lgani uchun kerakli kengaytmaning o'zini yozib qo'yamiz
    if not file.content_type == "video/mpeg":
        file.filename = f"{filename}.{supported_types[file.content_type]}"
    return file
