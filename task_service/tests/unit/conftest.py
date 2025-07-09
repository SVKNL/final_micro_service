
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.models.user import User
from tests.fixtures.db_mocks.tasks import TASKS
from tests.fixtures.db_mocks.users import USERS
from tests.utils import bulk_save_models


@pytest_asyncio.fixture
async def setup_tasks(transaction_session: AsyncSession) -> None:
    """Creates companies that will only exist within the session."""
    await bulk_save_models(transaction_session, Task, TASKS)


@pytest_asyncio.fixture
async def setup_users(transaction_session: AsyncSession) -> None:
    """Creates users that will only exist within the session."""
    await bulk_save_models(transaction_session, User, USERS)
