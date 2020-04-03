import datetime

from fastapi import Query

from app.schemas.authentication import SessionFilters
from app.schemas.filters import AreaFilters, TimeFilters


def get_city_filters(area_name: str = Query("Chongqing", alias="city"), ) -> AreaFilters:
    """
    获取传递的城市信息
    :param area_name: 城市名称
    :return:
    """
    return AreaFilters(
        name=area_name
    )


def get_area_filters(area_name: str = Query("China", alias="country"), ) -> AreaFilters:
    """
    获取传递的区域信息
    :param area_name: 区域名称
    :return:
    """
    return AreaFilters(
        name=area_name
    )


def get_time_filters(
        stime: str = Query(datetime.date.today().strftime('%Y-%m-%d'), alias="stime"),
        etime: str = Query((datetime.date.today() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d'),
                           alias="etime"), ) -> TimeFilters:
    """
    获取传递的时间区间信息
    :param stime: 开始时间
    :param etime: 截至时间
    :return:
    """
    return TimeFilters(
        stime=stime,
        etime=etime
    )


def get_session_filters(session: str = Query("", alias="session"), ) -> SessionFilters:
    return SessionFilters(
        session=session,
    )
