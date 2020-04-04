from pydantic import BaseModel, Field


class AreaFilters(BaseModel):
    name: str = Field("", min_length=1)


class AllowEmptyAreaFilters(BaseModel):
    name: str = Field("")


class TimeFilters(BaseModel):
    stime: str = Field("")
    etime: str = Field("")


class DetailFilters(BaseModel):
    detail: bool = Field(bool)


class PDateTimeFilters(BaseModel):
    date: str = Field("")
