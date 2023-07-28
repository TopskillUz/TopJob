from pydantic import BaseModel


class IBaseModel(BaseModel):
    class Config:
        from_attributes = True


class BaseListResponseSchema(BaseModel):
    page_number: int
    page_size: int
    num_pages: int
    total_results: int
