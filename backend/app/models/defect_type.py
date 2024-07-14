from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class DefectType(Base):
    __tablename__ = 'defect_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    color: Mapped[str] = mapped_column(String())


__all__ = ['DefectType']
