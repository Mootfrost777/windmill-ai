import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, Response, File, UploadFile, HTTPException
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from app.dependencies import get_session
from app.models import Image, ScanResult, Defect
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse
import io


router = APIRouter(prefix='/stats')


@router.get('/report')
async def get_report(user_id: int,
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

    defects = resp.scalars().all()
    defect_types = []
    colors = []
    sizes = []
    for defect in defects:
        sizes.append(defect.type.name)
        if defect.type.name not in defect_types:
            defect_types.append(defect.type.name)
            colors.append(defect.type.color)
    x = 0.5 + np.arange(len(set(sizes)))

    fig, ax = plt.subplots()
    ax.bar(x=x, height=pd.Series(sizes).value_counts(), label=defect_types, color=colors)
    plt.title('Статистика повреждений на изображениях')
    ax.set_ylabel("Кол-во")
    ax.set_xlabel("Тип дефекта")
    ax.set_xticks(x, defect_types)
    for i, val in zip(x, pd.Series(sizes).value_counts()):
        plt.text(i, val + 0.05, str(val), fontsize=8)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    return Response(content=buf.getvalue(), media_type="image/png")
