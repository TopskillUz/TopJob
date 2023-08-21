from uuid import UUID

from fastapi import APIRouter, Response

import crud
from models import Sphere
from schemas.admin import sphere_schema
from utils.deps import PaginationDep, SearchArgsDep, current_user_dep

router = APIRouter()


@router.get("/list/", response_model=sphere_schema.AListResponseSchema)
def get_sphere_paginated_list(
        pagination: PaginationDep,
        search_args: SearchArgsDep,
        current_user: current_user_dep("read_sphere")
):
    spheres, pagination_data = crud.sphere.get_paginated_list(**pagination, **search_args,
                                                              search_fields=["title", "description"])
    results = [sphere_schema.ASphereReadSchema.model_validate(sphere) for sphere in spheres]
    return sphere_schema.AListResponseSchema(**pagination_data, results=results)


@router.get("/{sphere_id}", response_model=sphere_schema.ASphereReadSchema)
def get_sphere(sphere_id: int, current_user: current_user_dep("read_sphere")):
    sphere = crud.sphere.get_obj(where={Sphere.id: sphere_id})
    return sphere


@router.post("/create", response_model=sphere_schema.ASphereReadSchema)
def create_sphere(payload: sphere_schema.ASphereCreateSchema,
                  current_user: current_user_dep("create_sphere")):
    sphere = crud.sphere.create(payload)
    return sphere


@router.put("/{sphere_id}", response_model=sphere_schema.ASphereReadSchema)
def update_sphere(sphere_id: int, payload: sphere_schema.ASphereUpdateSchema,
                  current_user: current_user_dep("update_sphere")):
    sphere = crud.sphere.get_obj(where={Sphere.id: sphere_id})
    sphere = crud.sphere.update(sphere.id, payload)
    return sphere


@router.delete("/{sphere_id}")
def delete_sphere(sphere_id: int, current_user: current_user_dep("delete_sphere")):
    crud.sphere.delete(sphere_id)
    return Response(status_code=204)
