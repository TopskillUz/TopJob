from uuid import UUID

from fastapi import APIRouter, Response

import crud
from models import Resume
from schemas.admin import resume_schema
from utils.deps import PaginationDep, SearchArgsDep, current_user_dep

router = APIRouter()


@router.get("/list/", response_model=resume_schema.AListResponseSchema)
def get_resume_paginated_list(
        pagination: PaginationDep,
        search_args: SearchArgsDep,
        current_user: current_user_dep("read_resume")
):
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'job_title', 'country', 'city',
                     'address', 'zipcode', 'nationality', 'driving_license', 'place_of_residence',
                     'professional_summary', 'hobbies']
    resumes, pagination_data = crud.resume.get_paginated_list(**pagination, **search_args, search_fields=search_fields)
    results = [resume_schema.AResumeReadSchema.model_validate(resume) for resume in resumes]
    return resume_schema.AListResponseSchema(**pagination_data, results=results)


@router.get("/{resume_id}", response_model=resume_schema.AResumeReadSchema)
def get_resume(resume_id: UUID, current_user: current_user_dep("read_resume")):
    resume = crud.resume.get_obj(where={Resume.id: resume_id})
    return resume


@router.put("/{resume_id}", response_model=resume_schema.AResumeReadSchema)
def update_resume(resume_id: UUID, payload: resume_schema.AResumeUpdateSchema,
                  current_user: current_user_dep("update_resume")):
    resume = crud.resume.get_obj(where={Resume.id: resume_id})
    resume = crud.resume.update_fields(resume, payload)
    return resume


@router.delete("/{resume_id}")
def delete_resume(resume_id: UUID, current_user: current_user_dep("delete_resume")):
    crud.resume.delete(resume_id)
    return Response(status_code=204)
