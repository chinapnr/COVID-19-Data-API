from pydantic import BaseModel

from app.schemas.const import SUCCESS


class BaseResponse(BaseModel):
    code: str = SUCCESS
    message : str = "success"