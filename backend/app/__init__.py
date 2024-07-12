import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.db import engine
from app.models import Base
import logging

from app.routes import image_router, ml_router
from app.ml import load_models

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(image_router)
app.include_router(ml_router)


@app.on_event('startup')
async def startup():
    load_models()


__all__ = ['app']

