from fastapi import APIRouter

from endpoints.site.routers import resume_router, auth_router

site_router = APIRouter()

site_router.include_router(resume_router.router, prefix="/resume", tags=["Resume"])
site_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
