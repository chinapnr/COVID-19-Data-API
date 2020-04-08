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
from app.schemas.filters import RegionFilters, DateFilters, Hmtfilters, AllowEmptyFilters

router = APIRouter()


@router.get("/region", response_model=InfectionRegionInResponse, name="infection:region")
async def infection_region(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        region_filters: RegionFilters = Depends(get_region_filters),
        date_filters: DateFilters = Depends(get_date_filters),
        hmt_filters: Hmtfilters = Depends(get_hmt_filters),
) -> InfectionRegionInResponse:
    logger.info(
        f"received parameters, token:{token}, region_filters:{region_filters}, "
        f"date_filters: {date_filters}, hmt_filters:{hmt_filters}")

    # 判断日期
    date_filters = check_date_filter(date_filters)
    # 判断 htm
    hmt_filters = check_htm_filter(hmt_filters, region_filters)
    try:
        data = dict()
        data["region"] = {region_filters.name: {}}

        region_data = Covid19.get_infection_region_data(
            db=db, country=region_filters.name, start_date=date_filters.start_date,
            end_date=date_filters.end_date,
            hmt=hmt_filters.include_hmt
        )
        for _d in region_data:
            if not data.get("region").get(region_filters.name).get(str(_d.update_date)):
                data.get("region").get(region_filters.name).update(
                    {
                        str(_d.update_date): {
                            "confirmed_add": _d.confirmed_add,
                            "deaths_add": _d.deaths_add,
                            "recovered_add": _d.recovered_add,
                            "confirmed": _d.confirmed,
                            "deaths": _d.deaths,
                            "recovered": _d.recovered
                        }
                    }
                )
            else:
                data["region"][region_filters.name][str(_d.update_date)]["confirmed_add"] += _d.confirmed_add
                data["region"][region_filters.name][str(_d.update_date)]["deaths_add"] += _d.deaths_add
                data["region"][region_filters.name][str(_d.update_date)]["recovered_add"] += _d.recovered_add
                data["region"][region_filters.name][str(_d.update_date)]["confirmed"] += _d.confirmed
                data["region"][region_filters.name][str(_d.update_date)]["deaths"] += _d.deaths
                data["region"][region_filters.name][str(_d.update_date)]["recovered"] += _d.recovered
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)
    return InfectionRegionInResponse(
        data=data
    )


@router.get("/region/detail", response_model=InfectionRegionDetailInResponse, name="infection:region detail")
async def infection_region_detail(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        region_filters: RegionFilters = Depends(get_region_filters),
        date_filters: DateFilters = Depends(get_date_filters),
        hmt_filters: Hmtfilters = Depends(get_hmt_filters),
) -> InfectionRegionDetailInResponse:
    logger.info(
        f"received parameters, token:{token}, region_filters:{region_filters}, "
        f"date_filters: {date_filters}, hmt_filters:{hmt_filters}")

    # 判断日期
    date_filters = check_date_filter(date_filters)
    # 判断 htm
    hmt_filters = check_htm_filter(hmt_filters, region_filters)
    try:
        data = dict({"area": {}})
        area_data = Covid19.get_infection_country_area_data(
            db=db, country=region_filters.name, start_date=date_filters.start_date,
            end_date=date_filters.end_date,
            hmt=hmt_filters.include_hmt
        )
        for _d in area_data:
            if (str(_d.province_en) == "Recovered"):
                continue
            if not data.get("area").get(str(_d.province_en)):
                # 城市不存在
                data.get("area").update({str(_d.province_en): {
                    str(_d.update_date): {
                        "confirmed_add": _d.confirmed_add,
                        "deaths_add": _d.deaths_add,
                        "recovered_add": _d.recovered_add,
                        "confirmed": _d.confirmed,
                        "deaths": _d.deaths,
                        "recovered": _d.recovered
                    }
                }
                })
            else:
                # 城市已经存在
                if data.get("area").get(_d.province_en).get(str(_d.update_date)):
                    # 日期已经存在
                    data["area"][str(_d.province_en)][str(_d.update_date)]["confirmed_add"] += _d.confirmed_add
                    data["area"][str(_d.province_en)][str(_d.update_date)]["deaths_add"] += _d.deaths_add
                    data["area"][str(_d.province_en)][str(_d.update_date)]["recovered_add"] += _d.recovered_add
                    data["area"][str(_d.province_en)][str(_d.update_date)]["confirmed"] += _d.confirmed
                    data["area"][str(_d.province_en)][str(_d.update_date)]["deaths"] += _d.deaths
                    data["area"][str(_d.province_en)][str(_d.update_date)]["recovered"] += _d.recovered
                else:
                    # 日期不存在
                    data.get("area").get(_d.province_en).update({
                        str(_d.update_date): {
                            "confirmed_add": _d.confirmed_add,
                            "deaths_add": _d.deaths_add,
                            "recovered_add": _d.recovered_add,
                            "confirmed": _d.confirmed,
                            "deaths": _d.deaths,
                            "recovered": _d.recovered
                        }
                    })

    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return InfectionRegionDetailInResponse(
        data=data
    )


@router.get("/area", response_model=InfectionCityInResponse, name="infection:area")
async def infection_area(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        country_filters: AllowEmptyFilters = Depends(get_allow_empty_region_filters),
        area_filters: RegionFilters = Depends(get_area_filters),
        time_filters: DateFilters = Depends(get_date_filters),
) -> InfectionCityInResponse:
    logger.info(f"received parameters, token:{token}, area_filters:{area_filters}, time_filters: {time_filters}")

    try:
        city_detail = InfectionCityNoNameModel()
        city_data = Covid19.get_infection_city_data(
            db=db, city=area_filters.name, stime=time_filters.start_date, etime=time_filters.end_date,
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
        db: Session = Depends(get_db)
) -> InfectionGlobalDataInResponse:
    logger.info(f"received parameters, token:{token}")

    try:
        global_detail = GlobalDataModel()
        global_data = Covid19.get_infection_global_data(db=db)
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
