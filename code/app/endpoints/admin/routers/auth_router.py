from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.babel_config import _
from exceptions import CustomValidationError
from schemas.admin import auth_schema
from utils.deps import topskill_login, get_users_me
from utils.token import Token

router = APIRouter()


@router.post('/jwt/login', summary="Login API", response_model=auth_schema.ATokenSchema)
def login(payload: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Check if the user exist
    tokens = topskill_login(username=payload.username, password=payload.password)
    if not tokens:
        raise CustomValidationError(_('Username or password incorrect!'))

    user_data = get_users_me(access_token=tokens['access_token'])
    if not user_data:
        raise CustomValidationError(_('Invalid token!'))

    access_token = Token.create_access_token(user_data['id'])
    refresh_token = Token.create_refresh_token(user_data['id'])

    # Send both access and refresh
    return auth_schema.ATokenSchema(
        token_type='bearer',
        access_token=access_token,
        refresh_token=refresh_token,
    )
