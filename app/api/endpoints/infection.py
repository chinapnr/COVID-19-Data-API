from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fishbase.fish_logger import logger
from fastapi.security.api_key import APIKey

from app.db import get_db
from app.schemas.common import *
from app.schemas.infection import *
from app.models.covid import Covid19
from app.schemas.const import SYSTEM_ERROR
from app.schemas.errors import CustomException
from app.api.endpoints.authentication import get_api_key
from app.schemas.filters import AreaFilters, TimeFilters, DetailFilters, AllowEmptyAreaFilters

router = APIRouter()


@router.get("/country", response_model=InfectionCountryInResponse, name="infection:country")
async def infection_country(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        country_filters: AreaFilters = Depends(get_country_filters),
        time_filters: TimeFilters = Depends(get_time_filters),
        detail_filters: DetailFilters = Depends(get_detail_filters),
) -> InfectionCountryInResponse:
    logger.info(f"received parameters, token:{token}, area_filters:{country_filters}, time_filters: {time_filters}")

    try:
        data = InfectionCountryModel()
        # 查询国家数据信息，城市 area 为 []
        country_data = Covid19.get_infection_country_data(
            db=db, country=country_filters.name, stime=time_filters.stime,
            etime=time_filters.etime
        )
        if country_data:
            data.name = country_filters.name
            data.confirmed_add = country_data[0].confirmed_add
            data.deaths_add = country_data[0].deaths_add
            data.recovered_add = country_data[0].recovered_add
            data.area = []
        if detail_filters.detail:
            # 查询国家数据信息，包含城市 area 信息
            detail_city_data = Covid19.get_infection_country_city_data(
                db=db, country=country_filters.name, stime=time_filters.stime, etime=time_filters.etime
            )
            for _d in detail_city_data:
                data.area.append({
                    "name": _d.province_en,
                    "confirmed_add": _d.confirmed_add,
                    "deaths_add": _d.deaths_add,
                    "recovered_add": _d.recovered_add,
                })
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)
    return InfectionCountryInResponse(
        data=data
    )


@router.get("/city", response_model=InfectionCityInResponse, name="infection:city")
async def infection_city(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        country_filters: AllowEmptyAreaFilters = Depends(get_allow_empty_country_filters),
        area_filters: AreaFilters = Depends(get_area_filters),
        time_filters: TimeFilters = Depends(get_time_filters),
) -> InfectionCityInResponse:
    logger.info(f"received parameters, token:{token}, area_filters:{area_filters}, time_filters: {time_filters}")

    try:
        city_detail = InfectionCityNoNameModel()
        city_data = Covid19.get_infection_city_data(
            db=db, city=area_filters.name, stime=time_filters.stime, etime=time_filters.etime,
            country=country_filters.name
        )
        if city_data:
            city_detail.confirmed_add = city_data[0].confirmed_add if city_data[0].confirmed_add else 0
            city_detail.deaths_add = city_data[0].deaths_add if city_data[0].deaths_add else 0
            city_detail.recovered_add = city_data[0].recovered_add if city_data[0].recovered_add else 0

    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)
    return InfectionCityInResponse(
        data=city_detail
    )


@router.get("/global", response_model=InfectionGlobalDataInResponse, name="infection:global")
async def infection_global_detail(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        time_filters: TimeFilters = Depends(get_time_filters)
) -> InfectionGlobalDataInResponse:
    logger.info(f"received parameters, token:{token}")

    try:
        global_detail = GlobalDataModel()
        global_data = Covid19.get_infection_global_data(db=db, stime=time_filters.stime, etime=time_filters.etime)
        for _d in global_data:
            global_detail.country.update({
                _d.country_en: {
                    "confirmed_add": _d.confirmed_add,
                    "deaths_add": _d.deaths_add,
                    "recovered_add": _d.recovered_add
                }
            })
            global_detail.confirmed_add += _d.confirmed_add
            global_detail.deaths_add += _d.deaths_add
            global_detail.recovered_add += _d.recovered_add
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return InfectionGlobalDataInResponse(
        data={"global": global_detail}
    )
