
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, created_at, intpk
from ..schemas.user import UserDB


class User(Base):
    __tablename__ = 'user'

    id: Mapped[intpk]
    password: Mapped[str]
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)
    email: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True)
    created_at: Mapped[created_at]

    def to_schema(self) -> UserDB:
        return UserDB(**self.__dict__)