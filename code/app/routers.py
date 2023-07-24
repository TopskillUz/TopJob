import logging

from fastapi import FastAPI

from app.core.config import settings
from core.handler import add_handlers
from core.middleware import add_middlewares
from endpoints.admin.api import admin_router
from endpoints.site.api import site_router

app = FastAPI(title="TopJob API",
              docs_url="/docs",
              openapi_url="/api/docs",
              debug=settings.DEBUG)

admin_app = FastAPI(debug=settings.DEBUG)
site_app = FastAPI(debug=settings.DEBUG)

app.mount(path=f'{settings.API_PREFIX}/admin', app=admin_app)
admin_app.include_router(admin_router)

app.mount(path=f'{settings.API_PREFIX}/site', app=site_app)
site_app.include_router(site_router)


add_middlewares(app=app)
add_handlers(app=app)