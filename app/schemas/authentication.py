from pydantic import BaseModel, Field

from app.models import BaseResponse


class EmailFilters(BaseModel):
    """
    区域过滤
    """
    email: str = Field(default="example@gmail.com")


class AuthenticationRegisterInResponse(BaseResponse):
    data: dict
