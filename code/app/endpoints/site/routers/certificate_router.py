from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form, Response
from pydantic import BaseModel

import crud
from models import CertificateBlock
from schemas.site.certificate_block_schema import ICertificateBlockReadSchema
from utils.deps import minio_auth
from utils.minio_client import MinioClient

router = APIRouter()


@router.get("/list/", response_model=list[ICertificateBlockReadSchema])
def get_certificate(resume_id: UUID | None = None):
    where = {}
    if resume_id:
        where.update({CertificateBlock.resume_id: resume_id})
    certificates = crud.certificate.get_list(where=where)
    return certificates


@router.get("/{certificate_id}", response_model=ICertificateBlockReadSchema)
def get_certificate(certificate_id: UUID):
    certificate = crud.certificate.get_obj(where={CertificateBlock.id: certificate_id})
    return certificate


@router.post("/", response_model=ICertificateBlockReadSchema)
def create_certificate(
        minio_client: Annotated[MinioClient, Depends(minio_auth)],
        resume_id: Annotated[UUID, Form()],
        name: Annotated[str | None, Form()] = None,
        file: Annotated[UploadFile | None, File()] = None,
        page: Annotated[int, Form(ge=1)] = 1
):
    certificate = crud.certificate.create(create_data={"page": page, "resume_id": resume_id})
    if name:
        certificate = crud.certificate.update(certificate.id, update_data={"name": name})
    if file:
        crud.certificate.update_file(certificate, file, minio_client)
    return certificate


@router.put("/{certificate_id}", response_model=ICertificateBlockReadSchema)
def update_certificate(
        certificate_id: UUID,
        minio_client: Annotated[MinioClient, Depends(minio_auth)],
        name: Annotated[str | None, Form()] = None,
        file: Annotated[UploadFile | None, File()] = None,
):
    certificate = crud.certificate.get_obj(where={CertificateBlock.id: certificate_id})
    if name:
        crud.certificate.update(certificate.id, update_data={"name": name})
    if file:
        crud.certificate.update_file(certificate, file, minio_client)
    return certificate


@router.delete("/{certificate_id}")
def delete_certificate(certificate_id: UUID):
    crud.certificate.delete(certificate_id)
    return Response(status_code=204)


class Item(BaseModel):
    name: str
    description: str


class FileUpload(BaseModel):
    files: list[UploadFile]


@router.post("/upload/")
def upload_files_and_json(item: Item, files: FileUpload):
    # Access the JSON data
    name = item.name
    description = item.description

    # Process the uploaded files
    for file in files.files:
        file_content = file.read()
        # Do something with the file_content, like saving it to disk or processing it.
        print(file_content, name, description)
    return {"message": "Files and JSON body uploaded successfully."}
