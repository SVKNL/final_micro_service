from src.schemas.task import TaskCreateRequest

TEST_TASK_SERVICE_ADD_ONE: list[dict] = [{
    'data': TaskCreateRequest(
          title='title_test2',
          description='descr_test2',
          status='in_progress',
          author_id=1,
          assignee_id=1,
          sprint_id=None,
          group_id=None,
          column_id=None,
          board_id=None,
    ),
        'expected_data': {
            'task_id': 2,
        },
},
    ]

TEST_TASK_SERVICE_GET_ALL_BY_QUERY: list[dict] = [
    {
        'data': {
            'status': 'todo',
        },
        'expected_data': {
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
    },
]
