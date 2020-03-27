from app.models import BaseResponse

from typing import List
from typing import Mapping

from pydantic import BaseModel


class CityModel(BaseModel):
    """
    城市
    """
    name: str  # 城市名称
    code: str  # 城市code


class InfectionDailyModel(BaseModel):
    """
    每日疫情数据信息
    """
    diagnose: int  # 确诊数
    cure: int  # 治愈数
    death: int  # 死亡数
    treatment: int  # 治疗数
    weather: str = None  # 天气信息


class InfectionCityModel(InfectionDailyModel, CityModel):
    """
    城市疫情数据信息
    """
    pass


class CountryModel(BaseModel):
    """
    国家
    """
    name: str  # 国家名称
    code: str  # 国家code
    city: List[InfectionCityModel]  # 国家包含得城市信息（包含疫情数据）


class _CountryModel(BaseModel):
    """
    国家
    """
    name: str  # 国家名称
    code: str  # 国家code
    city: List[CityModel]  # 国家包含得城市信息（不包含疫情数据）


class InfectionCountryModel(BaseModel):
    """
    国家疫情数据信息
    """
    city: List[InfectionCityModel]  # 国家所包含得城市信息


class GlobalModel(BaseModel):
    """
    全球（大洲）疫情数据信息
    """
    name: str  # 洲名称
    code: str  # 洲code
    country: Mapping[str, CountryModel]  # 洲包含的国家信息


class _GlobalModel(BaseModel):
    """
    全球（大洲）疫情数据信息
    """
    name: str  # 洲名称
    code: str  # 洲code
    country: Mapping[str, _CountryModel]  # 洲包含的国家信息(不包含疫情数据)


class InfectionAreaModel(BaseModel):
    """
    全球（包含各大洲）受感染得城市信息（不包含疫情数据）
    """
    globals: Mapping[str, _GlobalModel]


class InfectionGlobalModel(InfectionAreaModel):
    """
    全球（包含各大洲）疫情数据信息
    """
    globals: Mapping[str, GlobalModel]


class InfectionDailyInResponse(BaseResponse):
    """
    每日新增数据
    """
    data: Mapping[str, InfectionDailyModel]


class InfectionAreaInResponse(BaseResponse):
    data: InfectionAreaModel


class InfectionCountryInResponse(BaseResponse):
    data: InfectionCountryModel


class InfectionCityInResponse(BaseResponse):
    data: InfectionCityModel


class InfectionGlobalInResponse(BaseResponse):
    data: InfectionGlobalModel
