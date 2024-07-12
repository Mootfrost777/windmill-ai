from datetime import datetime

from app.models import Base
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class ScanResult(Base):
    __tablename__ = 'scan_results'
    id: Mapped[int] = mapped_column(primary_key=True)

    # defect_id: Mapped[int] = mapped_column(ForeignKey('defects.id'))
    defects: Mapped[List['Defect']] = relationship(back_populates='scan_result')

    image_id: Mapped[int] = mapped_column(ForeignKey('images.id'))
    image: Mapped['Image'] = relationship(back_populates='scan_results')

    scanned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


__all__ = ['ScanResult']
