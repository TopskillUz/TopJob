from fastapi import APIRouter

import crud
from schemas.site import sphere_schema
from utils.deps import PaginationDep, SearchArgsDep, current_user_dep

router = APIRouter()


@router.get("/list/", response_model=sphere_schema.IListResponseSchema)
def get_sphere_paginated_list(
        pagination: PaginationDep,
        search_args: SearchArgsDep,
        # current_user: current_user_dep("read_sphere")
):
    spheres, pagination_data = crud.sphere.get_paginated_list(**pagination, **search_args,
                                                              search_fields=["title", "description"])
    results = [sphere_schema.ISphereReadSchema.model_validate(sphere) for sphere in spheres]
    return sphere_schema.IListResponseSchema(**pagination_data, results=results)
