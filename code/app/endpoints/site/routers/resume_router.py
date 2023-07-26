from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import true
from sqlalchemy.orm import class_mapper, RelationshipProperty

import crud
from models import Resume
from schemas.site import resume_schema

router = APIRouter()


@router.get("/{resume_id}", response_model=resume_schema.IResumeReadSchema)
def get_resume(resume_id: Optional[UUID] = None):
    resume = crud.resume.get(where={Resume.id: resume_id, Resume.is_active: true()})
    if not resume:
        resume = crud.resume.create({"id": resume_id})
    return resume


@router.put("/{resume_id}", response_model=resume_schema.IResumeReadSchema)
def update_resume(resume_id: UUID, payload: resume_schema.IResumeUpdateSchema):
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
