from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.utils import get_db
from app.schemas.infection import *
from app.schemas.filters import AreaFilters, TimeFilters
from app.schemas.common import get_area_filters, get_time_filters

router = APIRouter()


@router.get("/daily", response_model=InfectionDailyInResponse, name="infection:daily")
async def infection_daily(area_filters: AreaFilters = Depends(get_area_filters), ) -> InfectionDailyInResponse:
    """
    查询每日新增情况<br/>
    :param area_filters: 区域过滤条件<br/>
    :return:
    """
    print(area_filters)
    return InfectionDailyInResponse()


@router.get("/area", response_model=InfectionAreaInResponse, name="infection:area")
async def infection_area(time_filters: TimeFilters = Depends(get_time_filters), ) -> InfectionAreaInResponse:
    """
    查询发生过疫情的地区信息（包含洲，国家，地区的名称和code）<br/>
    :param time_filters: 时间过滤条件<br/>
    :return:
    """
    print(time_filters)
    return InfectionAreaInResponse()


@router.get("/country", response_model=InfectionCountryInResponse, name="infection:country")
async def infection_country(
        area_filters: AreaFilters = Depends(get_area_filters),
        time_filters: TimeFilters = Depends(get_time_filters), ) -> InfectionCountryInResponse:
    """
    查询每个国家的数据（包含 确诊，治愈，死亡，治疗，天气【若包含城市】）信息
    :param area_filters: 地区过滤条件<br/>
    :param time_filters: 时间过滤条件<br/>
    :return:
    """
    print(area_filters, time_filters)
    return InfectionCountryInResponse()


@router.get("/city", response_model=InfectionCityInResponse, name="infection:city")
async def infection_city(
        area_filters: AreaFilters = Depends(get_area_filters),
        city_filters: AreaFilters = Depends(get_area_filters),
        time_filters: TimeFilters = Depends(get_time_filters), ) -> InfectionCityInResponse:
    """
    查询每个国家每个城市的数据信息（包含 确诊，治愈，死亡，治疗，天气）<br/>
    :param area_filters: 区域过滤条件<br/>
    :param city_filters: 城市过滤条件<br/>
    :param time_filters: 时间过滤条件<br/>
    :return:
    """
    print(area_filters, time_filters, city_filters)
    return InfectionCityInResponse()


@router.get("/global", response_model=InfectionGlobalInResponse, name="infection:global")
async def infection_global(
        area_filters: AreaFilters = Depends(get_area_filters),
        city_filters: AreaFilters = Depends(get_area_filters),
        time_filters: TimeFilters = Depends(get_time_filters), ) -> InfectionGlobalInResponse:
    """
    查询每个大洲每个国家每个城市的数据信息（包含 确诊，治愈，死亡，治疗，天气）<br/>
    :param area_filters: 区域过滤条件<br/>
    :param city_filters: 城市过滤条件<br/>
    :param time_filters: 时间过滤条件<br/>
    :return:
    """
    print(area_filters, time_filters, city_filters)
    return InfectionGlobalInResponse()
