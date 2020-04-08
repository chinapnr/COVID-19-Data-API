from fastapi import APIRouter

from app.api.endpoints import ratio, infection, authentication, health, other

# 汇总各模块路由信息
api_router = APIRouter()

# api_router.include_router(ratio.router, tags=["ratio"], prefix="/ratio")
# api_router.include_router(health.router, tags=["health"], prefix="/health")
api_router.include_router(infection.router, tags=["infection"], prefix="/infection")
api_router.include_router(other.router, tags=["other"], prefix="/other")
api_router.include_router(authentication.router, tags=["authentication"], prefix="/authentication")
