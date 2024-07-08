from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from app.db import engine
from app.models import Base
import logging

from app.routes import image_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['127.0.0.1:5713'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(image_router)


# @app.on_event('startup')
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     logging.info('ok')


__all__ = ['app']

