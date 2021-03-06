from typing import List
from typing import Mapping

from pydantic import BaseModel

from app.schemas import BaseResponse


class InfectionCityNoNameModel(BaseModel):
    confirmed_add: int = 0
    deaths_add: int = 0
    recovered_add: int = 0


class InfectionCityModel(BaseModel):
    confirmed_add: int = 0
    deaths_add: int = 0
    recovered_add: int = 0
    name: str = ""


class InfectionRegionModel(BaseModel):
    name: str = ""
    confirmed_add: int = 0
    deaths_add: int = 0
    recovered_add: int = 0
    area: List[InfectionCityModel] = []


class InfectionRegionInResponse(BaseResponse):
    data: Mapping[str, Mapping[str, Mapping[str, Mapping[str, int]]]]


class InfectionRegionDetailInResponse(InfectionRegionInResponse):
    data: Mapping[str, Mapping[str, Mapping[str, Mapping[str, int]]]]


class InfectionCityInResponse(BaseResponse):
    data: InfectionCityNoNameModel


class InfectionGlobalInResponse(BaseResponse):
    data: Mapping[str, Mapping[str, Mapping[str, str]]]


class GlobalDataModel(BaseModel):
    last_update_date = ""
    confirmed_add: int = 0
    deaths_add: int = 0
    recovered_add: int = 0
    region: Mapping[str, Mapping[str, int]] = {}


class InfectionGlobalDataInResponse(BaseResponse):
    data: Mapping[str, GlobalDataModel]
