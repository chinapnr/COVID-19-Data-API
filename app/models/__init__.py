from pydantic import BaseModel

class BaseResponse(BaseModel):
    code: str = 9000
    response_id : str = ""