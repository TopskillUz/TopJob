from fastapi import APIRouter

from endpoints.admin.routers import resume_router, auth_router

admin_router = APIRouter()

admin_router.include_router(resume_router.router, prefix="/resume", tags=["Resume"])
admin_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
