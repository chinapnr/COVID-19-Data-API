from pydantic import BaseModel, Field


class RegionFilters(BaseModel):
    name: str = Field("", min_length=1)


class AllowEmptyFilters(BaseModel):
    name: str = Field("")


class DateFilters(BaseModel):
    start_date: str = Field("")
    end_date: str = Field("")


class Hmtfilters(BaseModel):
    include_hmt: bool = Field(bool)


class PopulationYearFilters(BaseModel):
    date: str = Field("")
