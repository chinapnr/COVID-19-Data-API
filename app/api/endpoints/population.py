from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fishbase.fish_logger import logger
from fastapi.openapi.models import APIKey

from app.schemas.errors import CustomException
from app.db import get_db
from app.schemas.const import SYSTEM_ERROR
from app.models.population import Population
from app.api.endpoints.authentication import get_api_key
from app.schemas.common import get_allow_empty_region_filters, get_population_year_filters
from app.schemas.filters import RegionFilters, PopulationYearFilters
from app.schemas.population import PopulationInResponse, PopulationModel

router = APIRouter()


@router.get("", response_model=PopulationInResponse, name="population:population")
async def population(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db),
        country_filters: RegionFilters = Depends(get_allow_empty_region_filters),
        population_year_filters: PopulationYearFilters = Depends(get_population_year_filters),
) -> PopulationInResponse:
    logger.info(f"received parameters, token:{token}")

    try:
        _population = list()
        population_data = Population.get_population(db=db, country=country_filters.name,
                                                    date=population_year_filters.date)
        for _d in population_data:
            _population.append(
                PopulationModel(
                    country_en=_d.country_en,
                    population_num=_d.population_num
                )
            )
    except Exception as e:
        logger.error(f"{SYSTEM_ERROR}: {e}")
        raise CustomException(SYSTEM_ERROR)

    return PopulationInResponse(
        data=_population
    )
