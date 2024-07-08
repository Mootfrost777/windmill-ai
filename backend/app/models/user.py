from app.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import String, ForeignKey


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16))
    password: Mapped[str] = mapped_column(String())

    images: Mapped[List['Image']] = relationship(back_populates='uploaded_by')


__all__ = ['User']
