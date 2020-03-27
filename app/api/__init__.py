from fastapi import APIRouter

from app.api.endpoints import ratio, infection

# 汇总各模块路由信息
api_router = APIRouter()
api_router.include_router(ratio.router, tags=["ratio"], prefix="/ratio")
api_router.include_router(infection.router, tags=["infection"], prefix="/infection")