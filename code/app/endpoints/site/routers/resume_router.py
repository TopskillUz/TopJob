from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends

import crud
from models import Resume
from schemas.site import resume_schema
from utils.deps import require_user

router = APIRouter()


@router.get("/{resume_id}", response_model=resume_schema.IResumeReadSchema)
def get_resume(current_user: Annotated[dict, Depends(require_user("read_user"))], resume_id: Optional[UUID] = None):
    resume = crud.resume.get(where={Resume.id: resume_id})
    if not resume:
        resume = crud.resume.create({"id": resume_id})
    return resume
