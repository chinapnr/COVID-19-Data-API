from fastapi import Query

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
        stime: str = Query("2020-03-19", alias="stime"),
        etime: str = Query("2020-03-26", alias="etime"), ) -> TimeFilters:
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
