import enum

from pydantic import BaseModel


class IBaseModel(BaseModel):
    class Config:
        from_attributes = True



