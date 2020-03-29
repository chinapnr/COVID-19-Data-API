from fastapi import FastAPI
from starlette.requests import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from fishbase.fish_logger import set_log_stdout

from app.api import api_router
from app.config import config
from app.config.config import API_V1_STR
from app.db.session import Session
from app.schemas.errors import http422_error_handler, http_error_handler, CustomException

app = FastAPI(title=config.PROJECT_NAME)
app.include_router(api_router, prefix=API_V1_STR)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    return response


@app.exception_handler(CustomException)
async def exception_handler(_: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


set_log_stdout()
