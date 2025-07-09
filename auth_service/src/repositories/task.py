from sqlalchemy import select

from src.models.task import Task
from src.utils.repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository[Task]):
    model = Task

    async def find_all(self, filter):
        query = select(self.model)
        if filter.status:

            query = query.where(self.model.status == (filter.status.value))

        if filter.author_id:
            query = query.where(self.model.author_id == filter.author_id)

        if filter.assignee_id:
            query = query.where(self.model.assignee_id == filter.assignee_id)
        res = await self.session.execute(query)
        res = res.scalars().all()
        return res
