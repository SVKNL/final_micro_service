from abc import ABC, abstractmethod

from src.database import async_session_maker
from src.repositories.task import TaskRepository
from src.repositories.user import UserRepository


class IUnitOfWork(ABC):
    user: type[UserRepository]
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
        self.user = UserRepository(self._session)
        self.task = TaskRepository(self._session)

    async def __aexit__(self, *args):
        await self.commit()
        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
