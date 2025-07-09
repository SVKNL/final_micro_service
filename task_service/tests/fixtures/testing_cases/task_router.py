from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase

TEST_TASK_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={
            'title': 'title_test1',
            'description': 'descr_test1',
            'status': 'todo',
            'author_id': 1,
            'assignee_id': 1,
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'task_id': 1,
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={
            'title': 'title_test1',
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={
            'title': 1,
            'description': 'descr_test1',
            'status': 'todo',
            'author_id': 1,
            'assignee_id': 1,
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={
            'title': 'title_test1',
            'description': 'descr_test1',
            'status': 'test',
            'author_id': 1,
            'assignee_id': 1,
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),

 ]

TEST_TASK_ROUTE_GET_MANY_BY_FILTER: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        data={'status': 'todo'},
        expected_status=HTTP_200_OK,
        expected_data=[{
                'id': 1,
                'description': 'descr_test1',
                'status': 'todo',
                'sprint_id': None,
                'group_id': None,
                'title': 'title_test1',
                'author_id': 1,
                'assignee_id': 1,
                'column_id': None,
                'board_id': None,
        }],
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        data={'status': 'test'},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Wrong request body',
    ),
]
TEST_TASK_ROUTE_GET_ONE: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/1',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
                'id': 1,
                'description': 'descr_test1',
                'status': 'todo',
                'sprint_id': None,
                'group_id': None,
                'title': 'title_test1',
                'author_id': 1,
                'assignee_id': 1,
                'column_id': None,
                'board_id': None,
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/101',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent company',
    ),
]

TEST_TASK_ROUTE_DELETE_ONE: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/1',
        headers={},
        expected_status=HTTP_200_OK,
        description='Positive case',
    ),
]
