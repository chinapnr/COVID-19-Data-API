from sqlalchemy.orm import Session
from fishbase.fish_crypt import FishMD5
from fishbase.fish_logger import logger
from fastapi.security import APIKeyHeader
from fishbase.fish_common import get_time_uuid
from fastapi import Security, APIRouter, Depends

from app.db import get_db
from app.models.user import CovidUser
from app.utils.email import EmailUtils
from app.schemas.authentication import *
from app.config.config import HEADER_KEY, EMAIL_CONTENT
from app.utils.bloom import BloomFilterUtils
from app.schemas.errors import CustomException
from app.schemas.const import HTTP_FORBIDDEN, EMAIL_ERROR

# 设置请求头参数参数信息
api_key_header = APIKeyHeader(name=HEADER_KEY, auto_error=False)

router = APIRouter()


async def get_api_key(token: str = Security(api_key_header), ):
    if token:
        return token
    else:
        raise CustomException(HTTP_FORBIDDEN, status_code=403)


@router.post("/register", response_model=AuthenticationRegisterInResponse, name="authentication:register")
async def authentication_register(
        register_filters: RegisterFilters,
        db: Session = Depends(get_db),
) -> AuthenticationRegisterInResponse:
    """
    获取接口调用凭证 <br/>
    email： 获取凭证的邮箱地址
    """

    logger.info(f"received parameters, register_filters:{register_filters}")

    bloom_filter = BloomFilterUtils()
    email = EmailUtils()

    if not register_filters or not email.check_email(register_filters.email):
        raise CustomException(EMAIL_ERROR, msg_dict={"error": "format is incorrect"})

    # 邮箱已认证
    if bloom_filter.contains(register_filters.email) or CovidUser.get_user(
            db=db,
            condition={CovidUser.email.key: register_filters.email}
    ):
        raise CustomException(EMAIL_ERROR, msg_dict={"error": "email has been certified"})

    # 发送 token 信息
    token = FishMD5.hmac_md5(register_filters.email, str(get_time_uuid()))
    send_status = email.send_mail(EMAIL_CONTENT.format(_Token=token), register_filters.email)
    if not send_status:
        raise CustomException(EMAIL_ERROR, msg_dict={"error": "failed to send"})

    # 保存，记录邮箱信息
    CovidUser.add_user(db=db, email=register_filters.email, token=token)
    bloom_filter.add(register_filters.email)

    return AuthenticationRegisterInResponse(
        data={
            "status": True
        }
    )
