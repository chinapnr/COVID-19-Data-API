import datetime

from fastapi import Query

from app.schemas.errors import CustomException
from app.schemas.const import PARAM_ERROR
from app.schemas.filters import RegionFilters, DateFilters, Hmtfilters, PopulationYearFilters, AllowEmptyFilters


def get_area_filters(area_name: str = Query("Chongqing", alias="area"), ) -> RegionFilters:
    """
    获取传递的城市信息
    :param area_name: 城市名称
    :return:
    """
    return RegionFilters(
        name=area_name
    )


def get_region_filters(area_name: str = Query("China", alias="region"), ) -> RegionFilters:
    """
    获取传递的区域信息
    :param area_name: 区域名称
    :return:
    """
    return RegionFilters(
        name=area_name
    )


def get_allow_empty_region_filters(area_name: str = Query("", alias="region"), ) -> AllowEmptyFilters:
    return AllowEmptyFilters(
        name=area_name
    )


def get_date_filters(
        start_date: str = Query("", alias="start_date"),
        end_date: str = Query("", alias="end_date"),
) -> DateFilters:
    return DateFilters(
        start_date=start_date,
        end_date=end_date
    )


def get_hmt_filters(include_hmt: str = Query(True, alias="include_hmt"), ) -> Hmtfilters:
    return Hmtfilters(
        include_hmt=include_hmt,
    )


def get_population_year_filters(
        p_date: str = Query(datetime.date.today().strftime('%Y'), alias="year"), ) -> PopulationYearFilters:
    """
    :param p_date:
    :return:
    """
    return PopulationYearFilters(
        date=p_date
    )


def check_date_filter(date_filters: DateFilters):
    # 判断日期
    if not date_filters.start_date and not date_filters.end_date:
        # 默认为最新数据
        date_filters.start_date = None
        date_filters.end_date = None

    elif date_filters.start_date and date_filters.end_date:
        # 自定义日期
        # 判断是否超过 10 天
        try:
            start_date = datetime.datetime.strptime(date_filters.start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(date_filters.end_date, "%Y-%m-%d")
        except Exception as _:
            raise CustomException(PARAM_ERROR, msg_dict={"error": "start_date or end_date is incorrect"})

        if (end_date - start_date).days > 10 or (end_date - start_date).days < 0:
            raise CustomException(
                PARAM_ERROR,
                msg_dict={
                    "error": "The difference between start_date and end_date cannot be greater than 10 or less than 0"
                }
            )
    elif date_filters.start_date and not date_filters.end_date:
        # 具体的一天(start_date 和 end_date 相同)
        date_filters.start_date = date_filters.start_date
        date_filters.end_date = date_filters.start_date
    else:
        raise CustomException(PARAM_ERROR, msg_dict={"error": "You can’t just enter the end_date"})

    return date_filters


def check_htm_filter(hmt_filters: Hmtfilters, region_filters: RegionFilters or AllowEmptyFilters):
    if region_filters.name != "China":
        hmt_filters.include_hmt = False
    return hmt_filters
