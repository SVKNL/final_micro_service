from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Base


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError


M = TypeVar('M', bound=Base)


class SQLAlchemyRepository(AbstractRepository, Generic[M]):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = (update(self.model).values(**data).
                filter_by(id=id).
                returning(self.model.id))
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self):
        query = select(self.model)
        res = await self.session.execute(query)
        res = res.scalars().all()
        return res

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        return res

    async def delete_one(self, id: int) -> bool:
        obj = await self.find_one(id=id)
        if obj:
            stmt = delete(self.model).filter_by(id=id)
            await self.session.execute(stmt)
            return True
        return False
