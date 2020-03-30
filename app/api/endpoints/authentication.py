import random
from sqlalchemy.orm import Session
from fishbase.fish_crypt import FishMD5
from fastapi.security import APIKeyHeader
from fastapi import Security, APIRouter, Depends

from app.db.utils import get_db
from app.models.user import COVID_USER
from app.config.config import HEADER_KEY
from app.schemas.authentication import AuthenticationRegisterInResponse, EmailFilters
from app.schemas.common import get_email_filters
from app.schemas.const import HTTP_FORBIDDEN, EMAIL_ERROR
from app.schemas.errors import CustomException

# 设置请求头参数参数信息
api_key_header = APIKeyHeader(name=HEADER_KEY, auto_error=False)

router = APIRouter()


@router.post("/register", response_model=AuthenticationRegisterInResponse, name="authentication:register")
async def infection_daily(
        db: Session = Depends(get_db),
        email_filters: EmailFilters = Depends(get_email_filters)
) -> AuthenticationRegisterInResponse:
    """
    获取 Token 信息<br/>
    :return:
    """
    if not email_filters:
        raise CustomException(EMAIL_ERROR)

    token = FishMD5.hmac_md5(email_filters.email, str(random.random()))
    COVID_USER.add_user(db=db, email=email_filters.email, token=token)
    return AuthenticationRegisterInResponse(
        data={
            "token": token
        }
    )


async def get_api_key(db: Session = Depends(get_db), token: str = Security(api_key_header), ):
    if token:
        if COVID_USER.get_user(db=db, token=token):
            return token
        else:
            raise CustomException(HTTP_FORBIDDEN, status_code=403)
    else:
        raise CustomException(HTTP_FORBIDDEN, status_code=403)
