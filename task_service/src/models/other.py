from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, intpk


class Board(Base):
    __tablename__ = 'board'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True)

    columns = relationship('Column',
                           back_populates='board',
                           )
    tasks = relationship(
        'Task',
        back_populates='board')


class Column(Base):
    __tablename__ = 'column'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)
    board_id: Mapped[int] = mapped_column(
        ForeignKey(
            'board.id',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    board = relationship(
        'Board',
        back_populates='columns')
    tasks = relationship(
        'Task',
        back_populates='column')


class Sprint(Base):
    __tablename__ = 'sprint'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False)

    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()

    tasks = relationship(
        'Task',
        back_populates='sprint')


class Group(Base):
    __tablename__ = 'group'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True)
    tasks = relationship(
        'Task',
        back_populates='group')
