from base64 import b64encode

from fishbase import gen_random_str
from sqlalchemy.orm import Session
from fishbase.fish_logger import logger
from fishbase.fish_crypt import FishMD5
from fastapi.security import APIKeyHeader
from fishbase.fish_common import get_time_uuid
from fastapi import Security, APIRouter, Depends, Body

from app.db.utils import get_db
from app.utils.email import EmailUtils
from app.models.user import COVID_USER
from app.utils.redis import RedisClient
from app.schemas.authentication import *
from app.utils.bloom import BloomFilterUtils
from app.schemas.errors import CustomException
from app.utils.captcha.captcha import CaptchaUtils
from app.schemas.common import get_session_filters
from app.config.config import HEADER_KEY, REDIS_CONFIG
from app.schemas.const import HTTP_FORBIDDEN, EMAIL_ERROR, CAPTCHA_ERROR

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
        db: Session = Depends(get_db),
        register_filters: RegisterFilters = Body(..., embed=True, alias="data")
) -> AuthenticationRegisterInResponse:
    """
    提交邮箱信息<br/>
    :return:
    """
    redis = RedisClient(**REDIS_CONFIG)
    bloom_filter = BloomFilterUtils()
    email = EmailUtils()

    if not register_filters:
        raise CustomException(EMAIL_ERROR)

    # 邮箱已认证
    if bloom_filter.contains(register_filters.email):
        raise CustomException(EMAIL_ERROR, msg_dict={"error": "email has been certified"})

    # 验证验证码
    session_detail = redis.get_json(register_filters.session)
    if not session_detail or session_detail.get("captcha") != register_filters.captcha:
        raise CustomException(CAPTCHA_ERROR, msg_dict={"error": "Incorrect captcha"})

    # 发送 token 信息
    token = FishMD5.hmac_md5(register_filters.email, str(get_time_uuid()))
    send_status = email.send_mail(f"Your authentication token is: {token}", register_filters.email)
    if not send_status:
        raise CustomException(EMAIL_ERROR, msg_dict={"error": "failed to send"})

    # 保存，记录邮箱信息
    COVID_USER.add_user(db=db, email=register_filters.email, token=token)
    bloom_filter.add(register_filters.email)

    return AuthenticationRegisterInResponse(
        data={
            "token": token
        }
    )


@router.get("/session", response_model=AuthenticationSessionInResponse, name="authentication:session")
async def authentication_session() -> AuthenticationSessionInResponse:
    """
    获取 session 信息
    :return:
    """
    return AuthenticationSessionInResponse(
        data=gen_random_str(max_length=20, min_length=20, has_digit=True)
    )


@router.get("/captcha", response_model=AuthenticationCaptchaInResponse, name="authentication:captcha")
async def authentication_captcha(
        session_filters: SessionFilters = Depends(get_session_filters),
) -> AuthenticationCaptchaInResponse:
    """
    获取 验证码 信息
    :return:
    """
    try:
        redis = RedisClient(**REDIS_CONFIG)
        captcha = CaptchaUtils()

        captcha_info = captcha.gen_code()
        image_file = captcha_info['image_file']
        image_base64 = b64encode(image_file.getvalue())
        image_file.close()

        redis.set_json(session_filters.session, {'captcha': captcha_info['code']}, 3600)
        return AuthenticationCaptchaInResponse(
            data=image_base64
        )
    except Exception as e:
        logger.error(f"get captcha error: {e}")
        raise CustomException(CAPTCHA_ERROR, msg_dict={"error": "get captcha error"})
