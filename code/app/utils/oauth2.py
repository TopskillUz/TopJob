from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/jwt/login",
    scheme_name="JWT",
    description="TopJob API JWT Auth",
)
