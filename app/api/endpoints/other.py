from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fishbase.fish_logger import logger
from fastapi.openapi.models import APIKey

from app.db import get_db
from app.models.covid import Covid19
from app.schemas.const import SYSTEM_ERROR
from app.models.population import Population
from app.schemas.errors import CustomException
from app.api.endpoints.authentication import get_api_key
from app.schemas.filters import RegionFilters, Hmtfilters
from app.schemas.common import get_allow_empty_region_filters, get_region_filters, get_hmt_filters
from app.schemas.population import PopulationInResponse, PopulationModel, RegionListInResponse, AreaListInResponse

router = APIRouter()


@router.get("/populations", response_model=PopulationInResponse, name="other:population")
async def population(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        country_filters: RegionFilters = Depends(get_allow_empty_region_filters),
) -> PopulationInResponse:
    """
    查询人口数据信息 <br/>
    region: 国家 (非必传，默认值查全部国家) <br/>
    """

    logger.info(f"received parameters, token:{token}, country_filters: {country_filters}")

    try:
        _population = list()
        population_data = Population.get_population(db=db, country=country_filters.name)
        for _d in population_data:
            _population.append(
                PopulationModel(
                    name=_d.country_en,
                    population_num=_d.population_num
                )
            )
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return PopulationInResponse(
        data=_population
    )


@router.get("/region_list", response_model=RegionListInResponse, name="other:region_list")
async def region_list(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db)
) -> RegionListInResponse:
    """
    查询所有国家 <br/>
    """

    logger.info(f"received parameters, token:{token}")

    try:
        region_data = Covid19.get_region_list(db=db)
        data = [_d[0] for _d in region_data if _d[0]]
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)
    return RegionListInResponse(
        data=data
    )


@router.get("/area_list", response_model=AreaListInResponse, name="other:area_list")
async def area_list(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        region_filters: RegionFilters = Depends(get_region_filters),
        hmt_filters: Hmtfilters = Depends(get_hmt_filters)
) -> AreaListInResponse:
    """
    查询指定国家下的所有地区 <br/>
    region: 国家 <br/>
    include_hmt: 是否包含港澳台（当 region 为 China 时有效，默认为 true）
    """

    logger.info(f"received parameters, token:{token}, region_filters:{region_filters}, hmt_filters: {hmt_filters}")

    try:
        area_data = Covid19.get_area_list(db=db, region=region_filters.name, hmt=hmt_filters.include_hmt)
        data = [_d[0] for _d in area_data if _d[0] and _d[0] != "Recovered"]
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)
    return AreaListInResponse(
        data=data
    )
