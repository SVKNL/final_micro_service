from fastapi import Depends

from src.schemas.user import CreateUserRequest
from src.utils.unit_of_work import UnitOfWork


class UsersService:
    def __init__(self, unit_of_work: UnitOfWork = Depends()):
        self.uow = unit_of_work

    async def add_user(self, user: CreateUserRequest):
        user_dict = user.model_dump()
        async with self.uow:
            user_id = await self.uow.user.add_one(user_dict)
            return user_id

    async def get_users(self):
        async with self.uow:
            users = await self.uow.user.find_all()
            return users

    async def get_by_username(self, username):
        async with self.uow:
            try:
                user = await self.uow.user.get_by_username(username)
                return user.to_schema()
            except Exception as e:
                print(e)
                return False
