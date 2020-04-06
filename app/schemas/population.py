from typing import List, Optional

from pydantic import BaseModel

from app.schemas import BaseResponse


class PopulationModel(BaseModel):
    """
    人口数据信息
    """
    name: Optional[str] = ""
    population_num: Optional[int] = 0


class PopulationInResponse(BaseResponse):
    data: List[PopulationModel]


class RegionListInResponse(BaseResponse):
    data: List[str]

class AreaListInResponse(BaseResponse):
    data: List[str]
