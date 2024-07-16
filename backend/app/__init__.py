import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.db import engine
from app.models import Base
import logging

from pathlib import Path

from app.routes import image_router, ml_router, stats_router
from app.ml import load_models
from app.config import config

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


Path(config.static_dir).mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=config.static_dir), name="static")
app.include_router(image_router)
app.include_router(ml_router)
app.include_router(stats_router)


@app.on_event('startup')
async def startup():

    load_models()


__all__ = ['app']

