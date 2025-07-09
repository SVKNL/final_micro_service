import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.fixtures import FakeTasksService
from tests.fixtures.testing_cases import task_service


class TestBaseService:
    class _BaseService(FakeTasksService):
        _repo = 'task'

    def __get_service(self, session: AsyncSession) -> FakeTasksService:
        return self._BaseService(session)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', task_service.TEST_TASK_SERVICE_ADD_ONE)
    async def test_add_task(
        self,
        transaction_session: AsyncSession,
        case: dict,
    ) -> None:
        service = self.__get_service(transaction_session)
        result = await service.add_task(case['data'])
        assert result == case['expected_data']['task_id']
