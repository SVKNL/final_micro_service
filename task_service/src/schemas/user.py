
from fastapi import Query
from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    full_name: str = Field(max_length=50)
    email: str = Field(max_length=50)


class UpdateUserRequest(CreateUserRequest):
    pass


class UserDB(BaseModel):
    id: int = Field(gt=0)
    full_name: str = Field(max_length=50)
    email: str = Field(max_length=50)


class UserFilterSchema(BaseModel):
   id: int | None = Query(None)
