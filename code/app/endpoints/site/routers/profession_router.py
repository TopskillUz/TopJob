from fastapi import APIRouter
from sqlalchemy import select, or_, func
from sqlalchemy.orm import contains_eager

import crud
from models import Profession, ProfessionTranslation
from schemas.site import profession_schema
from utils.deps import PaginationDep, SearchArgsDep

router = APIRouter()


@router.get("/list/", response_model=profession_schema.IListResponseSchema)
def get_profession_paginated_list(
        pagination: PaginationDep,
        search_args: SearchArgsDep,
        sphere_id: int | None = None
):
    query = select(Profession)
    if sphere_id:
        query = query.filter(Profession.sphere_id == sphere_id)

    search_fields = ['title']
    q = search_args['q'] or ""
    if q:
        query = query.join(ProfessionTranslation, ProfessionTranslation.profession_id == Profession.id).options(
            contains_eager(Profession.translations))
        query = query.filter(
            or_(
                *[getattr(func.lower(getattr(ProfessionTranslation, field)), 'op')("~")(q.lower())
                  for field in search_fields if q],
                # Course.slug.op("~")(q.lower()),
            )
        )
    else:
        query = query.filter(Profession.parent_id.is_(None))


    professions, pagination_data = crud.profession.get_paginated_list(query=query, **pagination, **search_args)
    results = [profession_schema.IProfessionReadSchema.model_validate(profession) for profession in professions]
    return profession_schema.IListResponseSchema(**pagination_data, results=results)
