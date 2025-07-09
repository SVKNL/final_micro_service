from datetime import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


created_at = Annotated[
    datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())")),
]


class Base(DeclarativeBase):
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        return f'<{self.__class__.__name__} {", ".join(cols)}>'
