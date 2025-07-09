from fastapi import APIRouter, Depends
from starlette import status

from src.api.v1.services.task import TasksService
from src.schemas.task import (
    TaskCreateRequest,
    TaskFilterSchema,
    TaskListResponse,
    TaskResponse,
    TaskUpdateRequest,
)

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks'],
)


@router.get('/')
async def get_tasks(
    filter: TaskFilterSchema = Depends(),
    service: TasksService = Depends(),
):
    tasks = await service.get_tasks(filter)
    return TaskListResponse(payload=tasks)


@router.get('/{id}')
async def get_task(
    id: int,
    service: TasksService = Depends(),
):
    task = await service.get_task(id)
    return TaskResponse(payload=task)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_task(
    task: TaskCreateRequest,
    service: TasksService = Depends(),
):
    task_id = await service.add_task(task)
    return {'payload': {'task_id': task_id}}


@router.patch('/{id}')
async def edit_task(
    id: int,
    task: TaskUpdateRequest,
    service: TasksService = Depends(),
):
    await service.edit_task(id, task)
    return {'ok': True}


@router.delete('/{id}')
async def delete_task(
        id: int,
        service: TasksService = Depends(),
):
    await service.delete_task(id)
    return {'ok': True}
