from typing import List, Optional
from typing import Mapping

from pydantic import BaseModel

from app.schemas import BaseResponse


class CityModel(BaseModel):
    """
    城市
    """
    name_ch: Optional[str] = ""  # 城市名称
    name_en: Optional[str] = ""  # 城市英文名
    code: Optional[str] = ""  # 城市code


class InfectionDailyModel(BaseModel):
    """
    每日疫情数据信息
    """
    diagnose: Optional[int] = 0  # 确诊数
    cure: Optional[int] = 0  # 治愈数
    death: Optional[int] = 0  # 死亡数
    # weather: str = None  # 天气信息


class InfectionCityModel(InfectionDailyModel, CityModel):
    """
    城市疫情数据信息
    """
    pass


class InfectionCityGroupByDateModel(InfectionDailyModel, CityModel):
    """
    城市疫情数据信息
    """
    date: Optional[str] = ""  # 日期信息


class CountryModel(BaseModel):
    """
    国家
    """
    name_ch: Optional[str] = ""  # 国家名称
    name_en: Optional[str] = ""  # 英文名
    code: Optional[str] = ""  # 国家code
    city: List[InfectionCityModel]  # 国家包含得城市信息（包含疫情数据）


class _CountryModel(BaseModel):
    """
    国家
    """
    name_ch: Optional[str] = ""  # 国家名称
    name_en: Optional[str] = ""  # 英文名
    code: Optional[str] = ""  # 国家code
    city: Mapping[str, CityModel]  # 国家包含得城市信息（不包含疫情数据）


class InfectionCountryModel(BaseModel):
    """
    国家疫情数据信息
    """
    city: List[InfectionCityModel]  # 国家所包含得城市信息


class InfectionCountryGroupByDateModel(BaseModel):
    """
    国家疫情数据信息
    """
    city: Mapping[str, List[InfectionCityGroupByDateModel]]


class GlobalModel(BaseModel):
    """
    全球（大洲）疫情数据信息
    """
    name_ch: Optional[str] = ""  # 洲名称
    name_en: Optional[str] = ""  # 英文名
    code: Optional[str] = ""  # 洲code
    country: Mapping[str, CountryModel]  # 洲包含的国家信息


class _GlobalModel(BaseModel):
    """
    全球（大洲）疫情数据信息
    """
    name_ch: Optional[str] = ""  # 洲名称
    name_en: Optional[str] = ""  # 英文名
    code: Optional[str] = ""  # 洲 code
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


class InfectionCountryDetailInResponse(BaseResponse):
    data: InfectionCountryGroupByDateModel


class InfectionCityInResponse(BaseResponse):
    data: InfectionCityModel


class InfectionCityDetailInResponse(BaseResponse):
    data: List[InfectionCityGroupByDateModel]


class InfectionGlobalInResponse(BaseResponse):
    data: dict


class InfectionGlobalDataInResponse(BaseResponse):
    data: List[dict]
