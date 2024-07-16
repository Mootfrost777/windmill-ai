from fastapi import APIRouter, Depends, Response, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.config import config

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from app.dependencies import get_session
from app.models import Image, ScanResult, Defect

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
    images = []
    for file in files:
        if file.content_type != 'image/jpeg':
            raise

        img_name = str(uuid4()) + Path(file.filename).suffix
        try:
            contents = file.file.read()
            with open(path.join(config.static_dir, img_name), 'wb') as f:
                f.write(contents)
        except Exception:
            return Response(None, 406)
        finally:
            file.file.close()
        img = Image(filename=img_name, name=Path(file.filename).stem, uploaded_by_id=1)
        session.add(img)
        await session.commit()
        await session.refresh(img)
        images.append(img)
    return images


@router.get('/defects')
async def get_defects(scan_id: int,
                      session: AsyncSession = Depends(get_session)):
    resp = await session.execute(
        select(Defect).options(joinedload(Defect.type)).where(Defect.scan_result_id == scan_id)
    )
    return resp.scalars().all()


@router.get('/scan_results')
async def get_scan_results(image_id: int,
                      session: AsyncSession = Depends(get_session)):
    resp = await session.execute(
        select(ScanResult).where(ScanResult.image_id == image_id)
    )
    return resp.scalars().all()


@router.get('/summary')
async def get_summary(user_id: int,
                      session: AsyncSession = Depends(get_session)):
    scan_result_alias = aliased(ScanResult)
    image_alias = aliased(Image)
    resp = await session.execute(
        select(Defect)
        .options(joinedload(Defect.type))
        .outerjoin(scan_result_alias, Defect.scan_result_id == scan_result_alias.id)
        .outerjoin(image_alias, scan_result_alias.image_id == image_alias.id)
        .where(image_alias.uploaded_by_id == user_id)
    )
    return resp.scalars().all()


__all__ = ['router']
