from uuid import UUID

from fastapi import APIRouter
from sqlalchemy import select, func

import crud
from models import SkillBlock
from schemas.site import skill_block_schema
from utils.deps import PaginationDep, SearchArgsDep

router = APIRouter()


@router.get("/list/", response_model=skill_block_schema.ISkillListResponseSchema)
def get_skills(pagination: PaginationDep, search_args: SearchArgsDep, resume_id: UUID | None = None):
    stmt = (
        select(SkillBlock)
        .distinct(
            func.lower(SkillBlock.name),
        )
        .order_by(
            func.lower(SkillBlock.name).asc()
        )
    )
    if resume_id:
        stmt = stmt.filter(SkillBlock.resume_id == resume_id)
    if search_args.get("q"):
        stmt = stmt.filter(
            SkillBlock.name.ilike(f"%{search_args.get('q')}%")
        )
    skills, pagination_data = crud.skill.get_paginated_list(query=stmt, **pagination, **search_args)
    results = [skill_block_schema.ISkillBlockReadSchema.model_validate(skill) for skill in skills]
    return skill_block_schema.ISkillListResponseSchema(**pagination_data, results=results)
