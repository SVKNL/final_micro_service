from datetime import datetime
from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    author_id: int
    assignee_id: int = None
    column_id: int | None = None
    sprint_id: int | None = None
    board_id: int | None = None
    group_id: int | None = None


class TaskUpdateRequest(TaskCreateRequest):
    pass


class TaskID(BaseModel):
    id: int


class TaskDB(BaseModel):
    id: int
    description: str | None
    status: TaskStatus
    created_at: datetime
    sprint_id: int | None
    group_id: int | None
    title: str
    author_id: int
    assignee_id: int
    column_id: int | None
    board_id: int | None


class TaskResponse(BaseModel):
    payload: TaskDB


class TaskFilterSchema(BaseModel):
    status: TaskStatus | None = Query(None)
    author_id: int | None = Query(None)
    assignee_id: int | None = Query(None)


class TaskListResponse(BaseModel):
    payload: list[TaskDB]
