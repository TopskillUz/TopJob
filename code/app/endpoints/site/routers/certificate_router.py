from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form, Response

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


@router.put("/{certificate_id}", response_model=ICertificateBlockReadSchema)
def update_certificate(
        certificate_id: UUID,
        minio_client: Annotated[MinioClient, Depends(minio_auth)],
        name: Annotated[str | None, Form()] = None,
        file: Annotated[UploadFile, File()] = None,
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
