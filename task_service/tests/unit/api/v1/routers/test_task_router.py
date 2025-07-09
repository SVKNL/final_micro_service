import pytest
from httpx import AsyncClient

from tests.fixtures.testing_cases import task_router
from tests.utils import RequestTestCase, prepare_payload, prepare_payload_for_multiple


class TestTaskRouter:

    @staticmethod
    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', task_router.TEST_TASK_ROUTE_CREATE_PARAMS)
    async def test_create(
        case: RequestTestCase,
        async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.post(case.url, json=case.data, headers=case.headers)
            assert response.status_code == case.expected_status
            assert prepare_payload(response) == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users', 'setup_tasks')
    @pytest.mark.parametrize('case', task_router.TEST_TASK_ROUTE_GET_ONE)
    async def test_get_task_by_id(
        case: RequestTestCase,
        async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.get(case.url, headers=case.headers)
            assert response.status_code == case.expected_status
            assert prepare_payload(response, exclude=['created_at']) == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users', 'setup_tasks')
    @pytest.mark.parametrize('case', task_router.TEST_TASK_ROUTE_GET_MANY_BY_FILTER)
    async def test_get_tasks_by_filter(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.get(case.url, params=case.data)
            assert response.status_code == case.expected_status
            assert prepare_payload_for_multiple(
                response, exclude=['created_at'],
            ) == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users', 'setup_tasks')
    @pytest.mark.parametrize('case', task_router.TEST_TASK_ROUTE_DELETE_ONE)
    async def test_delete_task_by_id(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.delete(case.url, headers=case.headers)
            assert response.status_code == case.expected_status
