from abc import ABC, abstractmethod
from types import TracebackType

from src.database import async_session_maker
from src.repositories.task import TaskRepository


class IUnitOfWork(ABC):
    task: type[TaskRepository]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.is_open = False

    async def __aenter__(self):
        self._session = async_session_maker()
        self.task = TaskRepository(self._session)
        self.is_open = True

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
        ) -> None:
        if not exc_type:
            await self._session.commit()
        else:
            await self.rollback()
        await self._session.close()
        self.is_open = False

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
