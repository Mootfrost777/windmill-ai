from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List


class ScanResult(Base):
    __tablename__ = 'scan_results'
    id: Mapped[int] = mapped_column(primary_key=True)

    defect_id: Mapped[int] = mapped_column(ForeignKey('defects.id'))
    defect: Mapped[List['Defect']] = relationship()

    image_id: Mapped[int] = mapped_column(ForeignKey('images.id'))
    image: Mapped['Image'] = relationship(back_populates='scan_results')


__all__ = ['ScanResult']
