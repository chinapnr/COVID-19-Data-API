import datetime

from fastapi import Query

from app.schemas.filters import AreaFilters, TimeFilters, DetailFilters, PDateTimeFilters, AllowEmptyAreaFilters


def get_area_filters(area_name: str = Query("Chongqing", alias="area"), ) -> AreaFilters:
    """
    获取传递的城市信息
    :param area_name: 城市名称
    :return:
    """
    return AreaFilters(
        name=area_name
    )


def get_country_filters(area_name: str = Query("China", alias="country"), ) -> AreaFilters:
    """
    获取传递的区域信息
    :param area_name: 区域名称
    :return:
    """
    return AreaFilters(
        name=area_name
    )


def get_allow_empty_country_filters(area_name: str = Query("", alias="country"), ) -> AllowEmptyAreaFilters:
    return AllowEmptyAreaFilters(
        name=area_name
    )


def get_time_filters(
        stime: str = Query((datetime.date.today() + datetime.timedelta(days=-7)).strftime('%Y-%m-%d'), alias="stime"),
        etime: str = Query(datetime.date.today().strftime('%Y-%m-%d'), alias="etime"), ) -> TimeFilters:
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


def get_detail_filters(detail: str = Query(False, alias="detail"), ) -> DetailFilters:
    """
    :param detail:
    :return:
    """
    return DetailFilters(
        detail=detail,
    )


def get_population_date_filters(
        p_date: str = Query(datetime.date.today().strftime('%Y'), alias="date"), ) -> PDateTimeFilters:
    """
    :param p_date:
    :return:
    """
    return PDateTimeFilters(
        date=p_date
    )
