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

add_middlewares(app=app)

admin_app = FastAPI(debug=settings.DEBUG)
site_app = FastAPI(debug=settings.DEBUG)

add_handlers(app=admin_app)
add_handlers(app=site_app)

app.mount(path=f'/topjob{settings.API_PREFIX}/admin', app=admin_app)
admin_app.include_router(admin_router)

app.mount(path=f'/topjob{settings.API_PREFIX}/site', app=site_app)
site_app.include_router(site_router)


@app.get("/url-list")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list
