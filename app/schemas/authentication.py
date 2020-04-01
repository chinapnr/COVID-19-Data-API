from pydantic import BaseModel, Field

from app.models import BaseResponse


class EmailFilters(BaseModel):
    """
    区域过滤
    """
    email: str = Field(default="example@gmail.com")


class SessionFilters(BaseModel):
    """
    """
    session: str = Field(default="")


class CaptchaFilters(BaseModel):
    """
    区域过滤
    """
    captcha: str = Field(default="")


class RegisterFilters(SessionFilters, CaptchaFilters, EmailFilters):
    pass


class AuthenticationRegisterInResponse(BaseResponse):
    data: dict


class AuthenticationCaptchaInResponse(BaseResponse):
    data: str


class AuthenticationSessionInResponse(BaseResponse):
    data: str
