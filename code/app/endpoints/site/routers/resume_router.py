from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi_sqlalchemy import db
from pydantic import AnyHttpUrl
from sqlalchemy import true

import crud
from models import Resume, CertificateBlock, Media
from schemas.site import resume_schema
from schemas.site.certificate_block_schema import ICertificateBlockReadSchema
from schemas.site.media_schema import IMediaShortReadSchema
from utils.deps import minio_auth, PaginationDep, SearchArgsDep, current_user_dep
from utils.minio_client import MinioClient

router = APIRouter()


@router.get("/list/", response_model=resume_schema.IListResponseSchema)
def get_resume_paginated_list(
        pagination: PaginationDep,
        search_args: SearchArgsDep,
        current_user: current_user_dep("read_resume")
):
    # columns = list(filter(lambda v: not v.endswith("_at"), Resume.__table__.columns.keys()))
    # print(columns)
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'job_title', 'country', 'city',
                     'address', 'zipcode', 'nationality', 'driving_license', 'place_of_residence', 'date_of_birth',
                     'professional_summary', 'hobbies']
    resumes, pagination_data = crud.resume.get_paginated_list(where={Resume.is_active: true()}, **pagination,
                                                              **search_args, search_fields=search_fields)
    results = [resume_schema.IResumeReadSchema.model_validate(resume) for resume in resumes]
    return resume_schema.IListResponseSchema(**pagination_data, results=results)


@router.get("/{resume_id}", response_model=resume_schema.IResumeReadSchema)
def get_resume(resume_id: UUID):
    resume = crud.resume.get(where={Resume.id: resume_id, Resume.is_active: true()})
    if not resume:
        resume = crud.resume.create({"id": resume_id})
    return resume


@router.put("/{resume_id}", response_model=resume_schema.IResumeReadSchema)
def update_resume(
        resume_id: UUID,
        payload: resume_schema.IResumeUpdateSchema,
):
    resume = crud.resume.get_obj(where={Resume.id: resume_id, Resume.is_active: true()})
    resume = crud.resume.update_fields(resume, payload)
    return resume


@router.put("/{resume_id}/upload/image", response_model=IMediaShortReadSchema | None)
def update_resume_image(
        resume_id: UUID,
        minio_client: Annotated[MinioClient, Depends(minio_auth)],
        image: Annotated[UploadFile, File] = File(None),
):
    resume = crud.resume.get_obj(where={Resume.id: resume_id, Resume.is_active: true()})
    res = crud.resume.update_image(resume, image, minio_client)
    return res


@router.put("/{resume_id}/certificate/update", response_model=list[ICertificateBlockReadSchema])
def update_resume_image(
        resume_id: UUID,
        minio_client: Annotated[MinioClient, Depends(minio_auth)],
        names: Annotated[list[str], Form(...)],
        files: Annotated[list[UploadFile | str], File(...)]
):
    resume = crud.resume.get_obj(where={Resume.id: resume_id, Resume.is_active: true()})
    certificates = [certificate.id for certificate in resume.certificates]

    for name, file_or_path in zip(names, files):
        if isinstance(file_or_path, str):
            media = crud.media.get_obj(where={Media.path: file_or_path})
            certificate = crud.certificate.get_obj(where={CertificateBlock.file_id: media.id})
            crud.certificate.update(certificate.id, update_data={"name": name})
            certificates.remove(certificate.id)
        else:
            obj = crud.certificate.create(create_data={"name": name, "resume_id": resume_id})
            crud.certificate.update_file(obj, file_or_path, minio_client)
    for certificate_id in certificates:
        certificate = crud.certificate.get_obj(where={CertificateBlock.id: certificate_id})
        db.session.delete(certificate)
    db.session.commit()
    db.session.refresh(resume)
    return resume.certificates
