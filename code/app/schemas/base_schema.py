import enum


class TokenType(str, enum.Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"
