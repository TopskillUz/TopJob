from fastapi import APIRouter

from endpoints.admin.routers import resume_router, auth_router, sphere_router, profession_router

admin_router = APIRouter()

admin_router.include_router(resume_router.router, prefix="/resume", tags=["Resume"])
admin_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
admin_router.include_router(sphere_router.router, prefix="/sphere", tags=["Sphere"])
admin_router.include_router(profession_router.router, prefix="/profession", tags=["Profession"])
