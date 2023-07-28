import time

from fastapi import Request
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from core.babel_config import babel, ALLOWED_LANGUAGES
from core.config import settings


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, some_attribute: str = 'Test'):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        # print(request)

        start_time = time.time()
        # process the request and get the response
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response


def add_middlewares(app):
    # localization middleware
    @app.middleware("http")
    async def get_accept_language(request: Request, call_next):
        lang = request.headers.get("accept-language", ALLOWED_LANGUAGES[0])
        if lang not in ALLOWED_LANGUAGES:
            lang = ALLOWED_LANGUAGES[0]
        babel.locale = lang
        response = await call_next(request)
        return response

    # Allowed hosts middleware
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "*", "10.12.0.74"]
    )
    # process time middleware
    app.add_middleware(ProcessTimeMiddleware)

    # async database middleware
    app.add_middleware(
        DBSessionMiddleware,
        db_url=settings.SYNC_DATABASE_URI,
        engine_args={
            "echo": False,
            "pool_pre_ping": True,
            "pool_size": settings.POOL_SIZE,
            "max_overflow": 64,
        },
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

    # async def catch_exceptions_middleware(request: Request, call_next):
    #     try:
    #         return await call_next(request)
    #     except Exception:
    #         # you probably want some kind of logging here
    #         return Response("Internal server error2", status_code=500)
    #
    # app.middleware('http')(catch_exceptions_middleware)
