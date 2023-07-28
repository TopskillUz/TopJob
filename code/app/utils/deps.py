from typing import Optional, Annotated
from uuid import UUID

import redis
import requests
from fastapi import Depends, HTTPException, Query, Request
from redis import Redis

from core.babel_config import _
from core.config import settings
from models.enums import TokenType

from utils.minio_client import MinioClient
from utils.oauth2 import oauth2_scheme
from utils.token import Token


def check_permission(user_data: dict, perm_title: str):
    # Check if superuser
    if user_data['is_superuser']:
        return

    # Check role permissions
    permissions = []
    permissions.extend([perm['title'] for role in user_data['roles'] for perm in role['permissions']])
    permissions.extend([perm['title'] for perm in user_data['self_permissions']])

    if perm_title not in permissions:
        raise HTTPException(403, _("You have not a permission to perform action."))


def topskill_login(username: str, password: str, as_admin: Optional[bool] = False) -> dict | None:
    url = f"{settings.TOPSKILL_BASE_URL}/api/v1/{'admin' if as_admin else 'site'}/auth/jwt/login"
    r = requests.post(url, data={
        "username": username,
        "password": password
    })
    if r.status_code == 200 and r.json():
        return r.json()


def get_users_me(access_token: str):
    r = requests.get(f"{settings.TOPSKILL_BASE_URL}/api/v1/site/users/me", headers={
        "Authorization": f"Bearer {access_token}"
    })
    if r.status_code == 200 and r.json():
        return r.json()


def get_user_data(user_id: UUID | str, access_token: Optional[str] = None) -> dict | None:
    if not access_token:
        data = topskill_login(username=settings.TOPSKILL_ADMIN_USERNAME,
                              password=settings.TOPSKILL_ADMIN_PASSWORD,
                              as_admin=True)
        access_token = data['access_token']

    r = requests.get(f"{settings.TOPSKILL_BASE_URL}/api/v1/admin/users/get/{user_id}", headers={
        "Authorization": f"Bearer {access_token}"
    })
    if r.status_code == 200 and r.json():
        return r.json()


def get_redis_client() -> Redis:
    redis_client = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis_client


def require_user(perm_title: str):
    def get_current_user(
            request: Request,
            token: Annotated[str, Depends(oauth2_scheme)],
            redis_client: Annotated[Redis, Depends(get_redis_client)],
    ) -> dict:
        payload = Token.decode_token(token=token)

        if not payload['type'] == 'access':
            raise HTTPException(401, _("Incorrect token"))

        user_id = payload['sub']

        valid_access_tokens = Token.get_valid_tokens(
            redis_client, user_id, TokenType.ACCESS
        )

        if valid_access_tokens and token not in valid_access_tokens:
            raise HTTPException(401, _("Could not validate credentials"))

        user_data = get_user_data(user_id=user_id)

        if not user_data:
            raise HTTPException(401, _('User not exists'))

        # Check if user verified his email
        if not user_data['is_verified']:
            raise HTTPException(403, _('Please verify your account!'))

        # check permission
        check_permission(user_data, perm_title)
        return user_data

    return get_current_user


CurrentUserDep = Annotated[dict, Depends(require_user("read_user"))]


def paginated_data_arguments(
        page_number: int | None = Query(default=1, ge=1),
        page_size: int | None = Query(default=10, ge=1),
        order_by: str | None = Query(default='created_at'),
        desc: bool | None = Query(default=True)
):
    return {
        "page_number": page_number,
        "page_size": page_size,
        "order_by": order_by,
        "desc": desc,
    }


PaginationDep = Annotated[dict, Depends(paginated_data_arguments)]


def list_data_arguments(
        order_by: Optional[str] = Query(default='created_at'),
        desc: Optional[bool] = Query(default=True)
):
    return {
        "order_by": order_by,
        "desc": desc,
    }


def search_arguments(
        q: Optional[str] = Query(default=None)
):
    return {"q": q}


SearchArgsDep = Annotated[dict, Depends(search_arguments)]


def minio_auth() -> MinioClient:
    minio_client = MinioClient(
        access_key=settings.BUCKET_ACCESS_KEY,
        secret_key=settings.BUCKET_SECRET_KEY,
        bucket_name=settings.BUCKET_NAME,
        minio_url=settings.BUCKET_URL,
    )
    return minio_client
#
#
# def eskiz_auth() -> EskizSmsClient:
#     sms_client = EskizSmsClient(
#         email=settings.ESKIZ_EMAIL,
#         password=settings.ESKIZ_PASSWORD
#     )
#     return sms_client
