from fastapi import HTTPException
from fastapi.params import Depends
from starlette.status import HTTP_404_NOT_FOUND

from src.schemas.task import TaskCreateRequest, TaskDB, TaskUpdateRequest
from src.utils.service import transaction_mode
from src.utils.unit_of_work import UnitOfWork


class TasksService:
    def __init__(self, unit_of_work: UnitOfWork = Depends()):
        self.uow = unit_of_work

    @transaction_mode
    async def add_task(self, task: TaskCreateRequest) -> TaskDB:
        tasks_dict = task.model_dump()
        async with self.uow:
            task_id = await self.uow.task.add_one(tasks_dict)
            return task_id

    @transaction_mode
    async def get_tasks(self, filter):
        async with self.uow:
            tasks = await self.uow.task.find_all(filter)
            return [task.to_schema() for task in tasks]

    @transaction_mode
    async def get_task(self, task_id):
        async with self.uow:
            task = await self.uow.task.get_one(task_id)
            if task is None:
                raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Task not found')
            return task.to_schema()

    @transaction_mode
    async def edit_task(self, task_id: int, task: TaskUpdateRequest):
        tasks_dict = task.model_dump()
        async with self.uow:
            await self.uow.task.edit_one(task_id, tasks_dict)

    @transaction_mode
    async def delete_task(self, task_id: int):
        async with self.uow:
            await self.uow.task.delete_one(task_id)

    @transaction_mode
    async def get_tasks_watched_and_executed_count(self, user_id):
        async with self.uow:
            await self.uow.task.get_watched_and_executed_count(user_id)
