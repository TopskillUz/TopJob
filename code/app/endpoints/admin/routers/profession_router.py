from uuid import UUID

from fastapi import APIRouter, Response
from sqlalchemy import null, not_, select

import crud
from models import Profession
from schemas.admin import profession_schema
from utils.deps import PaginationDep, SearchArgsDep, current_user_dep

router = APIRouter()


@router.get("/list/", response_model=profession_schema.AListResponseSchema)
def get_profession_paginated_list(
        pagination: PaginationDep,
        search_args: SearchArgsDep,
        current_user: current_user_dep("read_profession"),
        is_parent: bool = None,
):
    query = select(Profession)
    if is_parent:
        query = query.filter(Profession.parent_id.is_(None))
    else:
        query = query.filter(Profession.parent_id.is_not(None))
    professions, pagination_data = crud.profession.get_paginated_list(query=query, **pagination, **search_args,
                                                                      search_fields=["title", "description"])
    results = [profession_schema.AProfessionReadSchema.model_validate(profession) for profession in professions]
    return profession_schema.AListResponseSchema(**pagination_data, results=results)


@router.get("/{profession_id}", response_model=profession_schema.AProfessionReadSchema)
def get_profession(profession_id: int, current_user: current_user_dep("read_profession")):
    profession = crud.profession.get_obj(where={Profession.id: profession_id})
    return profession


@router.post("/create", response_model=profession_schema.AProfessionReadSchema)
def create_profession(payload: profession_schema.AProfessionCreateSchema,
                      current_user: current_user_dep("create_profession")):
    profession = crud.profession.create(payload)
    return profession


@router.put("/{profession_id}", response_model=profession_schema.AProfessionReadSchema)
def update_profession(profession_id: int, payload: profession_schema.AProfessionUpdateSchema,
                      current_user: current_user_dep("update_profession")):
    profession = crud.profession.get_obj(where={Profession.id: profession_id})
    profession = crud.profession.update(profession.id, payload)
    return profession


@router.delete("/{profession_id}")
def delete_profession(profession_id: int, current_user: current_user_dep("delete_profession")):
    crud.profession.delete(profession_id)
    return Response(status_code=204)
