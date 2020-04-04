from typing import List, Optional

from pydantic import BaseModel

from app.schemas import BaseResponse


class PopulationModel(BaseModel):
    """
    人口数据信息
    """
    country_en: Optional[str] = ""
    population_num: Optional[int] = 0


class PopulationInResponse(BaseResponse):
    data: List[PopulationModel]
