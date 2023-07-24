import base64
import logging
from uuid import UUID
from datetime import timedelta, datetime
from typing import Optional, Union, Any

import jwt
from fastapi import HTTPException
from redis import Redis

from core.babel_config import _
from core.config import settings
from schemas.base_schema import TokenType


class Token:
    __REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN
    __ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
    __JWT_ALGORITHM = settings.JWT_ALGORITHM
    __JWT_PUBLIC_KEY = base64.b64decode(settings.JWT_PUBLIC_KEY).decode('utf-8')
    __JWT_PRIVATE_KEY = base64.b64decode(settings.JWT_PRIVATE_KEY).decode('utf-8')

    @classmethod
    def __create_token(cls, subject: str | Any, expires_time: int = None, token_type: str = None) -> str:
        if expires_time:
            expire = datetime.utcnow() + timedelta(minutes=expires_time)
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRES_IN
            )
        to_encode = {"exp": expire, "sub": str(subject), "type": token_type}
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=cls.__JWT_PRIVATE_KEY,
            algorithm=cls.__JWT_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def create_access_token(cls, subject: Union[str, Any], expires_time: int = __ACCESS_TOKEN_EXPIRES_IN) -> str:
        return cls.__create_token(subject=subject, expires_time=expires_time,
                                  token_type="access")

    @classmethod
    def create_refresh_token(cls, subject: Union[str, Any],
                             expires_time: int = __REFRESH_TOKEN_EXPIRES_IN) -> str:
        return cls.__create_token(subject=subject, expires_time=expires_time,
                                  token_type="refresh")

    @classmethod
    def get_valid_tokens(cls, redis_client: Redis, user_id: UUID, token_type: TokenType):
        token_key = f"user:{user_id}:{token_type}"
        valid_tokens = redis_client.smembers(token_key)
        return valid_tokens

    @classmethod
    def add_token_to_redis(
            cls,
            redis_client: Redis,
            user_id: UUID,
            token: str,
            token_type: TokenType,
            expire_time: Optional[int] = None,
    ):
        token_key = f"user:{user_id}:{token_type}"
        valid_tokens = cls.get_valid_tokens(redis_client, user_id, token_type)
        redis_client.sadd(token_key, token)
        if not valid_tokens:
            redis_client.expire(token_key, timedelta(minutes=expire_time))

    @classmethod
    def delete_tokens(cls, redis_client: Redis, user_id: UUID, token_type: TokenType):
        token_key = f"user:{user_id}:{token_type}"
        valid_tokens = redis_client.smembers(token_key)
        if valid_tokens is not None:
            redis_client.delete(token_key)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            payload = jwt.decode(token, cls.__JWT_PUBLIC_KEY, algorithms=[cls.__JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, _("Token expired. Get new one"))
        except jwt.InvalidTokenError:
            raise HTTPException(401, _("Invalid Token"))
        except Exception as e:
            logging.error(str(e))
            raise HTTPException(500, _("Internal server error"))
