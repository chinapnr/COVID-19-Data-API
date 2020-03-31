from sqlalchemy.orm import Session
from fishbase.fish_crypt import FishMD5
from fastapi.security import APIKeyHeader
from fishbase.fish_common import get_time_uuid
from fastapi import Security, APIRouter, Depends

from app.db.utils import get_db
from app.utils.email import EmailUtils
from app.models.user import COVID_USER
from app.config.config import HEADER_KEY
from app.utils.bloom import BloomFilterUtils
from app.schemas.errors import CustomException
from app.schemas.common import get_email_filters
from app.schemas.const import HTTP_FORBIDDEN, EMAIL_ERROR
from app.schemas.authentication import AuthenticationRegisterInResponse, EmailFilters

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
    bloom_filter = BloomFilterUtils()

    if not email_filters:
        raise CustomException(EMAIL_ERROR)

    # 邮箱已认证
    if bloom_filter.contains(email_filters.email):
        raise CustomException(EMAIL_ERROR, msg_dict={"error": "email has been certified"})

    # 发送 token 信息
    token = FishMD5.hmac_md5(email_filters.email, str(get_time_uuid()))
    send_status = EmailUtils.send_mail(f"Your authentication token is: {token}", email_filters.email)
    if not send_status:
        raise CustomException(EMAIL_ERROR, msg_dict={"error": "failed to send"})

    # 保存，记录邮箱信息
    COVID_USER.add_user(db=db, email=email_filters.email, token=token)
    bloom_filter.add(email_filters.email)

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
