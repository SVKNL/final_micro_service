from sqlalchemy import select

from src.models.task import User
from src.utils.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    model = User

    async def get_by_username(self, username: str):
        stmt = select(self.model).where(self.model.full_name == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()