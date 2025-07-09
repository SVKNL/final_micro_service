import enum
from datetime import date, datetime

from sqlalchemy import ForeignKey, String, Text, text, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas.task import TaskDB

from .base import Base, intpk, user_id



class TaskStatus(enum.Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'


class TaskWatchers(Base):
    __tablename__ = 'task_watchers'

    user_id: Mapped[user_id]
    task_id: Mapped[int] = mapped_column(
        ForeignKey('task.id', ondelete='CASCADE'),
        primary_key=True,
    )


class TaskExecutors(Base):
    __tablename__ = 'task_executors'

    user_id: Mapped[user_id]
    task_id: Mapped[int] = mapped_column(
        ForeignKey('task.id', ondelete='CASCADE'),
        primary_key=True,
    )


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


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TaskStatus]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        index=True,
    )
    author_id: Mapped[user_id]
    assignee_id: Mapped[user_id | None]
    column_id: Mapped[int | None] = mapped_column(
        ForeignKey('column.id'),
        nullable=True)
    sprint_id: Mapped[int | None] = mapped_column(
        ForeignKey('sprint.id'),
        nullable=True)
    board_id: Mapped[int | None] = mapped_column(
        ForeignKey('board.id'),
        nullable=True)
    group_id: Mapped[int | None] = mapped_column(
        ForeignKey('group.id'),
        nullable=True)
    column = relationship(
        'Column',
        back_populates='tasks')
    sprint = relationship(
        'Sprint',
        back_populates='tasks')
    group = relationship(
        'Group',
        back_populates='tasks')
    board = relationship('Board',
                         back_populates='tasks')
    watchers: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)
    executors: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=list)

    def to_schema(self) -> TaskDB:
        return TaskDB(**self.__dict__)
