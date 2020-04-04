from fastapi import APIRouter

from app.schemas import BaseResponse

router = APIRouter()


@router.head("", response_model=BaseResponse, name="health:health")
async def health():
    """
    健康检查
    """
    return BaseResponse()
