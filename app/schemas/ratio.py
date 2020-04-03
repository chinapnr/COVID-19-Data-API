from typing import List

from app.schemas import BaseResponse

from pydantic import BaseModel


class Gender(BaseModel):
    """
    性别
    """
    male: str = ""
    female: str = ""


class GenderRatioModel(Gender):
    """
    性别比例 Model
    """
    pass


class SarsNcovRatioModel(BaseModel):
    """
    Sars Ncov 比例 Model
    """
    sars: str
    ncov: str


class RehabilitationRatioModel(BaseModel):
    """
    治愈和死亡比例 Model
    """
    cure: str
    death: str


class GenderRatioInResponse(BaseResponse):
    """
    性别比例 Response
    """
    data: GenderRatioModel


class AgeRatioInResponse(BaseResponse):
    """
    年龄比例 Response
    """
    data: List[str]


class SarsNcovRatioInResponse(BaseResponse):
    """
    Sars NCOV比例 Response
    """
    data: SarsNcovRatioModel


class RehabilitationRatioResponse(BaseResponse):
    """
    治愈 死亡比例
    """
    data: RehabilitationRatioModel
