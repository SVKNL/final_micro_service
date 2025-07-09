import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import router


def create_fast_api_app() -> FastAPI:
    load_dotenv(find_dotenv('.env'))
    env_name = os.getenv('MODE', 'DEV')

    if env_name != 'PROD':
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
        )
    else:
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            docs_url=None,
            redoc_url=None,
        )

    fastapi_app.include_router(router, prefix='/api')
    return fastapi_app


app = create_fast_api_app()
