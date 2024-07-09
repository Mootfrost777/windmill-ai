from fastapi import APIRouter, Query, Depends
from typing import List

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.dependencies import get_session
from app.models import Image

from app.ml import bin_predict

router = APIRouter(prefix='/ml')


class ImageCheck(BaseModel):
    ids: list[int]


@router.post('/check_bin')
async def check_bin(req: ImageCheck,
                    session: AsyncSession = Depends(get_session)):
    resp = await session.execute(
        select(Image).where(Image.id.in_(req.ids))
    )
    images = resp.scalars().all()
    predicts = bin_predict([img.filename for img in images])
    for img, pred in zip(images, predicts):
        img.defective = pred
    await session.commit()
    return images




