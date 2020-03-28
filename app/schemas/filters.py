from pydantic import BaseModel, Field


class AreaFilters(BaseModel):
    """
    区域过滤
    """
    name: str = Field("", min_length=1)


class TimeFilters(BaseModel):
    """
    时间区间过滤
    """
    stime: str = Field("")
    etime: str = Field("")
