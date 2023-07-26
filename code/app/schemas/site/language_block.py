from pydantic import Field, field_validator

from schemas.base_schema import IBaseModel


class ILanguageBlockReadSchema(IBaseModel):
    name: str
    level: int = Field(gt=0, le=100)
    page: int

    @field_validator('level')
    def check_level(cls, v: int) -> int:
        if v % 10:
            raise ValueError('Must be divisible by 10 without a remainder')
        return v
