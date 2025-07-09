from fastapi.params import Depends

from src.schemas.task import TaskCreateRequest, TaskDB, TaskUpdateRequest
from src.utils.unit_of_work import UnitOfWork


class TasksService:
    def __init__(self, unit_of_work: UnitOfWork = Depends()):
        self.uow = unit_of_work

    async def add_task(self, task: TaskCreateRequest) -> TaskDB:
        tasks_dict = task.model_dump()
        async with self.uow:
            task_id = await self.uow.task.add_one(tasks_dict)
            return task_id

    async def get_tasks(self, filter):
        async with self.uow:
            tasks = await self.uow.task.find_all(filter)
            return [task.to_schema() for task in tasks]

    async def get_task(self, task_id):
        async with self.uow:
            task = await self.uow.task.get_one(task_id)
            return task.to_schema()

    async def edit_task(self, task_id: int, task: TaskUpdateRequest):
        tasks_dict = task.model_dump()
        async with self.uow:
            await self.uow.task.edit_one(task_id, tasks_dict)

    async def delete_task(self, task_id: int):
        async with self.uow:
            await self.uow.task.delete_one(task_id)
