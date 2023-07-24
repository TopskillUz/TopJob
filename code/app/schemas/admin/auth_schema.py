from pydantic import BaseModel


class ATokenSchema(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
