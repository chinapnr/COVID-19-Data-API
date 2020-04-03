from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fishbase.fish_logger import logger
from fastapi.openapi.models import APIKey

from app.db import get_db
from app.models.population import Population
from app.api.endpoints.authentication import get_api_key
from app.schemas.population import PopulationInResponse, PopulationModel

router = APIRouter()


@router.get("", response_model=PopulationInResponse, name="population:population")
async def population(
        token: APIKey = Depends(get_api_key),
        db: Session = Depends(get_db)
) -> PopulationInResponse:
    """
    查询所有国家人口数据信息 <br/>
    """
    logger.info(f"received parameters, token:{token}")

    _population = list()
    population_data = Population.get_population(db=db)
    for _d in population_data:
        _population.append(
            PopulationModel(
                country_en=_d.country_en,
                country_ch=_d.country_ch,
                population_num=_d.population_num
            )
        )
    return PopulationInResponse(
        data=_population
    )
