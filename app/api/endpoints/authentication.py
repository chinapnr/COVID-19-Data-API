import time
from base64 import b64encode

from fastapi import Security, APIRouter, Depends, Body
from fastapi.security import APIKeyHeader
from fishbase import gen_random_str
from fishbase.fish_common import get_time_uuid
from fishbase.fish_crypt import FishMD5
from fishbase.fish_logger import logger
from sqlalchemy.orm import Session

from app.config.config import HEADER_KEY
from app.db import get_db
from app.models.captcha import Captcha
from app.models.user import CovidUser
from app.schemas.authentication import *
from app.schemas.common import get_session_filters
from app.schemas.const import HTTP_FORBIDDEN, EMAIL_ERROR, CAPTCHA_ERROR
from app.schemas.errors import CustomException
from app.utils.bloom import BloomFilterUtils
from app.utils.captcha.captcha import CaptchaUtils
from app.utils.email import EmailUtils

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

    # 验证验证码
    captcha_info = Captcha.get_captcha_by_session(db=db, session=register_filters.session)
    if not captcha_info or captcha_info.captcha != register_filters.captcha:
        raise CustomException(CAPTCHA_ERROR, msg_dict={"error": "Incorrect captcha"})

    if int(time.time()) > int(captcha_info.expiration):
        raise CustomException(CAPTCHA_ERROR, msg_dict={"error": "captcha has expired"})

    # 发送 token 信息
    token = FishMD5.hmac_md5(register_filters.email, str(get_time_uuid()))
    send_status = email.send_mail(f"Your authentication token is: {token}", register_filters.email)
    if not send_status:
        raise CustomException(EMAIL_ERROR, msg_dict={"error": "failed to send"})

    # 保存，记录邮箱信息
    CovidUser.add_user(db=db, email=register_filters.email, token=token)
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
        db: Session = Depends(get_db),
        session_filters: SessionFilters = Depends(get_session_filters),
) -> AuthenticationCaptchaInResponse:
    """
    获取 验证码 信息
    :return:
    """
    logger.info(f"received parameters, session_filters:{session_filters}")

    if not session_filters.session:
        raise CustomException(CAPTCHA_ERROR, msg_dict={"error": "captcha must be filled"})

    try:
        captcha = CaptchaUtils()
        captcha_info = captcha.gen_code()
        image_file = captcha_info['image_file']
        image_base64 = b64encode(image_file.getvalue())
        image_file.close()

        Captcha.add_captcha(
            db=db,
            captcha=captcha_info['code'],
            session_id=session_filters.session,
            expiration=str(int(time.time()) + 1800)
        )
        return AuthenticationCaptchaInResponse(
            data=image_base64
        )
    except Exception as e:
        logger.error(f"get captcha error: {e}")
        raise CustomException(CAPTCHA_ERROR, msg_dict={"error": "get captcha error"})
