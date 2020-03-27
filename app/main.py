import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from app.api import api_router
from app.config import config
from app.config.config import API_V1_STR
from app.db.session import Session

app = FastAPI(title=config.PROJECT_NAME)
app.include_router(api_router, prefix=API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    try:
        response = await call_next(request)
        request.state.db.commit()
        return response
    except Exception as _:
        request.state.db.rollback()
    finally:
        request.state.db.close()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
