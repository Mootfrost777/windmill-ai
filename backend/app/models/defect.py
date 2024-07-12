from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey


class Defect(Base):
    __tablename__ = 'defects'
    id: Mapped[int] = mapped_column(primary_key=True)
    coordinates: Mapped[str] = mapped_column(String())
    confidence: Mapped[float] = mapped_column(Float())

    type_id: Mapped[int] = mapped_column(ForeignKey('defect_types.id'))
    type: Mapped['DefectType'] = relationship()

    scan_result_id: Mapped[int] = mapped_column(ForeignKey('scan_results.id'))
    scan_result: Mapped['ScanResult'] = relationship(back_populates='defects')


__all__ = ['Defect']
