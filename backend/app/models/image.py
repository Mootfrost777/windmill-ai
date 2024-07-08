from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, DateTime, func
from datetime import datetime
from typing import List


class Image(Base):
    __tablename__ = 'images'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    filename: Mapped[str] = mapped_column(String())
    defective: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    scan_results: Mapped[List['ScanResult']] = relationship(back_populates='image')

    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    uploaded_by: Mapped['User'] = relationship(back_populates='images')

    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


__all__ = ['Image']
