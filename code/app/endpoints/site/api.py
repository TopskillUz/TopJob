from fastapi import APIRouter

from endpoints.site.routers import (resume_router, auth_router, certificate_router, skill_router, profession_router,
                                    sphere_router)

site_router = APIRouter()

site_router.include_router(resume_router.router, prefix="/resume", tags=["Resume"])
site_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
site_router.include_router(certificate_router.router, prefix="/certificate", tags=["Certificate"])
site_router.include_router(skill_router.router, prefix="/skill", tags=["Skill"])
site_router.include_router(profession_router.router, prefix="/profession", tags=["Profession"])
site_router.include_router(sphere_router.router, prefix="/sphere", tags=["Sphere"])
