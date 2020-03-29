from fastapi import Security
from fastapi.security import APIKeyHeader

from app.config.config import HEADER_KEY
from app.schemas.const import HTTP_FORBIDDEN
from app.schemas.errors import CustomException

# 设置请求头参数参数信息
api_key_header = APIKeyHeader(name=HEADER_KEY, auto_error=False)


async def get_api_key(token: str = Security(api_key_header), ):
    if token:
        return token
    else:
        raise CustomException(HTTP_FORBIDDEN, status_code=403)
