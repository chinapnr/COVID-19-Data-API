from fastapi import APIRouter

from app.schemas import BaseResponse

router = APIRouter()


@router.get("", response_model=BaseResponse, name="health:health")
async def health():
    """
    健康页 <br/>
    """
    return BaseResponse()
