from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Query, Body
from sqlalchemy import true, select, or_, func, and_
from sqlalchemy.orm import contains_eager

import crud
from core.babel_config import _
from exceptions import CustomValidationError
from models import Resume, ResumeStatusEnum, SkillBlock
from schemas.site import resume_schema
from schemas.site.media_schema import IMediaShortReadSchema
from utils.deps import minio_auth, PaginationDep, SearchArgsDep
from utils.minio_client import MinioClient

router = APIRouter()


@router.get("/list/", response_model=resume_schema.IListResponseSchema)
def get_resume_paginated_list(
        pagination: PaginationDep,
        search_args: SearchArgsDep,
        profession_id: Annotated[int, Query()] = None
):
    # columns = list(filter(lambda v: not v.endswith("_at"), Resume.__table__.columns.keys()))
    # print(columns)
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'job_title',
                     'professional_summary', 'hobbies']
    q = search_args["q"] or ""

    query = (
        select(Resume)
        .filter(
            Resume.status == ResumeStatusEnum.PUBLISH
        )
        .filter(
            Resume.is_active == true()
        )
    )
    if q:
        query = query.filter(
            or_(
                *[getattr(func.lower(getattr(Resume, field)), 'op')("~")(q.lower())
                  for field in search_fields if q]
            )
        )

    if profession_id:
        query = query.filter(
            Resume.profession_id == profession_id
        )

    # if skills:
    #     query = query.join(
    #         Resume.skills
    #     ).filter(
    #         or_(
    #             *[func.lower(SkillBlock.name).op("~")(skill.lower()) for skill in skills]
    #         )
    #     )
    resumes, pagination_data = crud.resume.get_paginated_list(query=query, **pagination)
    results = [resume_schema.IResumeReadSchema.model_validate(resume) for resume in resumes]
    return resume_schema.IListResponseSchema(**pagination_data, results=results)


@router.get("/{resume_id}", response_model=resume_schema.IResumeReadSchema)
def get_resume(resume_id: UUID):
    resume = crud.resume.get_obj(where={Resume.id: resume_id, Resume.is_active: true()})
    return resume


@router.post("/create/{resume_id}", response_model=resume_schema.IResumeReadSchema)
def create_resume(resume_id: UUID,
                  profession_id: Annotated[int | None, Body(embed=True)] = None,
                  template_id: Annotated[int | None, Body(embed=True)] = None):
    resume = crud.resume.get(where={Resume.id: resume_id, Resume.is_active: true()})
    if not resume:
        if not profession_id or not template_id:
            raise CustomValidationError(_("profession_id and template_id are required!"))
        resume = crud.resume.create({"id": resume_id, "profession_id": profession_id, "template_id": template_id})
    return resume


@router.put("/{resume_id}", response_model=resume_schema.IResumeReadSchema)
def update_resume(
        resume_id: UUID,
        payload: resume_schema.IResumeUpdateSchema,
):
    allowed_statuses = [ResumeStatusEnum.DRAFT, ResumeStatusEnum.PRIVATE, ResumeStatusEnum.PENDING]
    if payload.status not in allowed_statuses:
        raise CustomValidationError(
            _("Invalid status. Available Statuses: {statuses}").format(statuses=allowed_statuses))
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
