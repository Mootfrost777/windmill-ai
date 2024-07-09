from fastapi import APIRouter, Depends, Response, File, UploadFile, HTTPException
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_session
from app.models import Image

from enum import Enum
from uuid import uuid4
from os import path
from pathlib import Path


router = APIRouter(prefix='/images')


class OrderBy(str, Enum):
    name = 'name'
    uploaded = 'uploaded_at'


class ImagesGetParams(BaseModel):
    user_id: int
    order_by: OrderBy = OrderBy.name
    descending: bool = False


@router.get('/')
async def get_images(params: ImagesGetParams = Depends(),
                     session: AsyncSession = Depends(get_session)):
    order_column = getattr(Image, params.order_by)
    if params.descending:
        order_column = order_column.desc()

    result = await session.execute(
        select(Image).order_by(order_column).where(Image.uploaded_by_id == params.user_id)
    )
    return result.scalars().all()


@router.post('/upload')
async def upload_images(files: list[UploadFile],
                        session: AsyncSession = Depends(get_session)):
    for file in files:
        if file.content_type != 'image/jpeg':
            raise

        img_name = str(uuid4()) + Path(file.filename).suffix
        try:
            contents = file.file.read()
            with open(path.join('static', img_name), 'wb') as f:
                f.write(contents)
        except Exception:
            return Response(None, 406)
        finally:
            file.file.close()
        session.add(Image(filename=img_name, name=Path(file.filename).stem, uploaded_by_id=1))
    await session.commit()
    return Response(None, 201)


__all__ = ['router']
