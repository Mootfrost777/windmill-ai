from fastapi import APIRouter, Query, Depends
from typing import List
from os import path

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import aliased

from app.dependencies import get_session
from app.models import Image, ScanResult, Defect
from app.ml import bin_predict, yolo_predict

router = APIRouter(prefix='/ml')


class ImageCheckRequest(BaseModel):
    ids: list[int]


@router.post('/check_bin')
async def check_bin(req: ImageCheckRequest,
                    session: AsyncSession = Depends(get_session)):
    resp = await session.execute(
        select(Image).where(Image.id.in_(req.ids))
    )
    images = resp.scalars().all()
    predicts = bin_predict([path.join('static', img.filename) for img in images])
    for img, pred in zip(images, predicts):
        img.defective = pred
    await session.commit()
    return images


@router.post('/check_yolo')
async def check_yolo(req: ImageCheckRequest,
                     session: AsyncSession = Depends(get_session)):
    resp = await session.execute(
        select(Image)#.where(Image.id.in_(req.ids))
    )

    images = resp.scalars().all()
    results = yolo_predict([path.join('static', img.filename) for img in images])
    resp = []
    for img_id, result in zip([x.id for x in images], results):
        scan_res = ScanResult(
            defects=result,
            image_id=img_id
        )
        session.add(scan_res)
        await session.commit()
        await session.refresh(scan_res)
        resp.append(scan_res)
    return resp





