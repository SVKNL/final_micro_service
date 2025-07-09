"""The package contains various data used in tests."""

__all__ = [
    'FakeTasksService',
    'FakeUnitOfWork',
    'FakeUsersService',
    'TasksService',
    'UsersService',
    'db_mocks',
    'testing_cases',
]

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.services.task import TasksService
from src.api.v1.services.user import UsersService
from src.repositories.task import TaskRepository
from src.repositories.user import UserRepository
from src.utils.unit_of_work import UnitOfWork
from tests.fixtures import db_mocks, testing_cases


class FakeUnitOfWork(UnitOfWork):
    """Test class for overriding the standard UnitOfWork.
    Provides isolation using transactions at the level of a single TestCase.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def __aenter__(self) -> None:
        self.task = TaskRepository(self._session)
        self.user = UserRepository(self._session)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.flush()


class FakeUsersService(UsersService):
    """..."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.uow = FakeUnitOfWork(session)


class FakeTasksService(TasksService):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.uow = FakeUnitOfWork(session)
