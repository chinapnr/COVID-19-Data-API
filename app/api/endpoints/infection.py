from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fishbase.fish_logger import logger
from fastapi.security.api_key import APIKey

from app.db import get_db
from app.schemas.infection import *
from app.models.covid import Covid19
from app.schemas.const import SYSTEM_ERROR
from app.schemas.errors import CustomException
from app.schemas.filters import AreaFilters, TimeFilters
from app.api.endpoints.authentication import get_api_key
from app.schemas.common import get_area_filters, get_time_filters, get_city_filters

router = APIRouter()


@router.get("/detail", response_model=InfectionDailyInResponse, name="infection:daily")
async def infection_daily(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        area_filters: AreaFilters = Depends(get_area_filters)
) -> InfectionDailyInResponse:
    """
    根据国家查询城市每日新增数据信息
    """
    logger.info(f"received parameters, token:{token}, area_filters:{area_filters}")
    try:
        data = dict()
        daily_data = Covid19.get_infection_daily_data(db=db, country=area_filters.name)
        for _d in daily_data:
            data.update({_d.province_en: InfectionDailyModel(
                diagnose=_d.confirmed_add,
                cure=_d.recovered_add,
                death=_d.deaths_add
            )})
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)
    return InfectionDailyInResponse(data=data)


@router.get("/area", response_model=InfectionGlobalInResponse, name="infection:area")
async def infection_area(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        time_filters: TimeFilters = Depends(get_time_filters)
) -> InfectionGlobalInResponse:
    """
    查询发生过疫情的地区信息（包含洲，国家，地区）
    """
    logger.info(f"received parameters, token:{token}, time_filters:{time_filters}")
    try:
        _globals = dict()
        _country = dict()
        _city = dict()

        area_data = Covid19.get_infection_area_data(db=db, stime=time_filters.stime, etime=time_filters.etime)
        for _d in area_data:
            if not _d.continents_en:
                continue

            if _d.continents_en not in _globals:
                _globals.update({_d.continents_en: {
                    "name_ch": _d.continents_ch,
                    "name_en": _d.continents_en,
                    "code": _d.continents_en
                }})

            if _d.country_en not in _country:
                _country.update({_d.country_en: {
                    "name_ch": _d.country_ch,
                    "name_en": _d.country_en,
                    "code": _d.country_en
                }})

            if _d.province_en not in _city:
                _city.update({_d.province_en: {
                    "name_ch": _d.province_ch,
                    "name_en": _d.province_en,
                    "code": _d.province_en
                }})
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return InfectionGlobalInResponse(
        data={
            "globals": _globals, "country": _country, "city": _city
        }
    )


@router.get("/country", response_model=InfectionCountryInResponse, name="infection:country")
async def infection_country(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        area_filters: AreaFilters = Depends(get_area_filters),
        time_filters: TimeFilters = Depends(get_time_filters), ) -> InfectionCountryInResponse:
    """
    查询每个国家每个城市一段时间内的汇总数据（包含 确诊，治愈，死亡）信息
    """
    logger.info(f"received parameters, token:{token}, area_filters:{area_filters}, time_filters: {time_filters}")
    try:
        city_data = list()
        country_data = Covid19.get_infection_country_data(
            db=db, country=area_filters.name, stime=time_filters.stime, etime=time_filters.etime
        )
        for _d in country_data:
            city_data.append(InfectionCityModel(
                diagnose=_d.sum_confirmed, cure=_d.sum_recovered, death=_d.sum_deaths,
                name_ch=_d.province_ch, name_en=_d.province_en, code=_d.province_en)
            )
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return InfectionCountryInResponse(
        data=InfectionCountryModel(
            city=city_data
        )
    )


@router.get("/country/detail", response_model=InfectionCountryDetailInResponse, name="infection:country detail")
async def infection_country_detail(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        area_filters: AreaFilters = Depends(get_area_filters),
        time_filters: TimeFilters = Depends(get_time_filters), ) -> InfectionCountryDetailInResponse:
    """
    查询每个国家每个城市一段时间内的明细数据（包含 确诊，治愈，死亡）信息
    """
    logger.info(f"received parameters, token:{token}, area_filters:{area_filters}, time_filters: {time_filters}")
    try:
        city_data = dict()
        country_detail_data = Covid19.get_infection_country_detail_data(
            db=db, country=area_filters.name, stime=time_filters.stime, etime=time_filters.etime
        )
        for _d in country_detail_data:
            current_city_group_date_model = InfectionCityGroupByDateModel(
                diagnose=_d.confirmed_add, cure=_d.recovered_add, death=_d.deaths_add, date=str(_d.update_date),
                name_ch=_d.province_ch, name_en=_d.province_en, code=_d.province_en)
            # 添加到 city_data 中
            if city_data.get(_d.province_en):
                city_data[_d.province_en].append(
                    current_city_group_date_model
                )
            else:
                city_data[_d.province_en] = [current_city_group_date_model]
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return InfectionCountryDetailInResponse(
        data=InfectionCountryGroupByDateModel(
            city=city_data
        )
    )


@router.get("/city", response_model=InfectionCityInResponse, name="infection:city")
async def infection_city(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        city_filters: AreaFilters = Depends(get_city_filters),
        time_filters: TimeFilters = Depends(get_time_filters), ) -> InfectionCityInResponse:
    """
    根据国家查询每个城市一段时间内的汇总数据信息（包含 确诊，治愈，死亡）
    """
    logger.info(f"received parameters, token:{token}, city_filters:{city_filters}, time_filters: {time_filters}")
    try:
        city_data = Covid19.get_infection_city_data(
            db=db, city=city_filters.name, stime=time_filters.stime, etime=time_filters.etime
        )
        if city_data:
            city_detail = InfectionCityModel(
                diagnose=city_data[0].sum_confirmed, cure=city_data[0].sum_recovered, death=city_data[0].sum_deaths,
                name_ch=city_data[0].province_ch, name_en=city_data[0].province_en, code=city_data[0].province_en
            )
        else:
            city_detail = InfectionCityModel()
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return InfectionCityInResponse(
        data=city_detail
    )


@router.get("/city/detail", response_model=InfectionCityDetailInResponse, name="infection:city detail")
async def infection_city_detail(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        city_filters: AreaFilters = Depends(get_city_filters),
        time_filters: TimeFilters = Depends(get_time_filters), ) -> InfectionCityDetailInResponse:
    """
    根据国家查询每个城市一段时间内的明细数据信息（包含 确诊，治愈，死亡）
    """
    logger.info(f"received parameters, token:{token}, city_filters:{city_filters}, time_filters: {time_filters}")
    city_detail = []
    try:
        city_detail_data = Covid19.get_infection_city_detail_data(
            db=db, city=city_filters.name, stime=time_filters.stime, etime=time_filters.etime
        )
        if city_detail_data:
            for _d in city_detail_data:
                city_detail.append(InfectionCityGroupByDateModel(
                    diagnose=_d.confirmed_add,
                    cure=_d.recovered_add,
                    death=_d.deaths_add,
                    name_ch=_d.province_ch,
                    name_en=_d.province_en,
                    code=_d.province_en,
                    date=str(_d.update_date)
                ))
        else:
            city_detail = [InfectionCityGroupByDateModel(
                diagnose=0,
                cure=0,
                death=0,
                name_ch="",
                name_en="",
                code="",
                date=""
            )]
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return InfectionCityDetailInResponse(
        data=city_detail
    )


@router.get("/global/detail", response_model=InfectionGlobalDataInResponse, name="infection:global")
async def infection_global_detail(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
) -> InfectionGlobalDataInResponse:
    """
    查询全球每个国家当日数据信息
    """
    logger.info(f"received parameters, token:{token}")

    global_data = list()
    try:
        global_detail_data = Covid19.get_infection_global_data(db=db)
        for _d in global_detail_data:
            global_data.append({
                "diagnose": _d.sum_confirmed,
                "cure": _d.sum_recovered,
                "death": _d.sum_deaths,
                "name_ch": _d.country_ch,
                "name_en": _d.country_en,
                "code": _d.country_en
            })
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return InfectionGlobalDataInResponse(
        data=global_data
    )
