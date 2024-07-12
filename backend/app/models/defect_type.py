from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey


class DefectType(Base):
    __tablename__ = 'defect_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String())


__all__ = ['DefectType']
