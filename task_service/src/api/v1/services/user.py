from fastapi import Depends

from src.schemas.user import CreateUserRequest
from src.utils.service import transaction_mode
from src.utils.unit_of_work import UnitOfWork


class UsersService:
    def __init__(self, unit_of_work: UnitOfWork = Depends()):
        self.uow = unit_of_work

    @transaction_mode
    async def add_user(self, user: CreateUserRequest):
        user_dict = user.model_dump()
        async with self.uow:
            user_id = await self.uow.user.add_one(user_dict)
            return user_id

    @transaction_mode
    async def get_users(self, filter):
        async with self.uow:
            users = await self.uow.user.find_all(filter)
            return users
