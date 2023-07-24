from pydantic import BaseModel


class ITokenSchema(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
