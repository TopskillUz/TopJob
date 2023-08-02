from typing import Optional, Annotated, Union, Any
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form, Body
from fastapi_sqlalchemy import db
from pydantic import Json, AfterValidator, BeforeValidator, WrapValidator
from pydantic_core.core_schema import ValidatorFunctionWrapHandler, ValidationInfo
from sqlalchemy import true
from sqlalchemy.orm import class_mapper, RelationshipProperty

import crud
from models import Resume
from schemas.site import resume_schema
from schemas.site.certificate_block_schema import ICertificateBlockReadSchema
from schemas.site.media_schema import IMediaShortReadSchema
from utils.deps import minio_auth, paginated_data_arguments, search_arguments, require_user, PaginationDep, \
    SearchArgsDep, CurrentUserDep
from utils.minio_client import MinioClient

router = APIRouter()


@router.get("/list/", response_model=resume_schema.IListResponseSchema)
def get_resume_paginated_list(
        pagination: PaginationDep,
        search_args: SearchArgsDep,
        current_user: CurrentUserDep
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
def get_resume(resume_id: Optional[UUID] = None):
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
        files: Annotated[list[UploadFile], File(...)]
):
    resume = crud.resume.get_obj(where={Resume.id: resume_id, Resume.is_active: true()})
    for certificate in resume.certificates:
        db.session.delete(certificate)
    db.session.commit()
    for name, file in zip(names[0].split(","), files):
        obj = crud.certificate.create(create_data={"name": name, "resume_id": resume_id})
        crud.certificate.update_file(obj, file, minio_client)
    db.session.refresh(resume)
    return resume.certificates
