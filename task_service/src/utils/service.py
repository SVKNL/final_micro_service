import functools
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any, Never, TypeVar, overload

from src.utils.unit_of_work import IUnitOfWork

T = TypeVar('T', bound=Callable[..., Awaitable[Any]])


@overload
def transaction_mode(_func: T) -> T: ...
@overload
def transaction_mode(*, auto_flush: bool) -> Callable[[T], T]: ...


def transaction_mode(_func: T | None = None, *, auto_flush: bool = False) -> T | Callable[[T], T]:
    """Wraps the function in transaction mode.
    Checks if the UnitOfWork context manager is open.
    If not, then opens the context manager and opens a transaction.
    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(self: AbstractService, *args: Any, **kwargs: Any) -> Any:
            if self.uow.is_open:
                res = await func(self, *args, **kwargs)
                if auto_flush:
                    await self.uow.flush()
                return res
            async with self.uow:
                return await func(self, *args, **kwargs)

        return wrapper

    if _func is None:  # Using with parameters: @transaction_mode(auto_flush=True)
        return decorator
    return decorator(_func)  # Using without parameters: @transaction_mode


class AbstractService(ABC):
    """An abstract class that implements CRUD operations at the service level."""

    uow: IUnitOfWork

    @abstractmethod
    async def add_one(self, *args: Any, **kwargs: Any) -> Never:
        """Adding one entry."""
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(self, *args: Any, **kwargs: Any) -> Never:
        """Adding one entry and getting the ID of this entry."""
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_obj(self, *args: Any, **kwargs: Any) -> Never:
        """Adding one entry and getting that entry."""
        raise NotImplementedError

    @abstractmethod
    async def bulk_add(self, *args: Any, **kwargs: Any) -> Never:
        """Bulk adding of entries."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_filter_one_or_none(self, *args: Any, **kwargs: Any) -> Never:
        """Get one entry for the given filter, if it exists."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_filter_all(self, *args: Any, **kwargs: Any) -> Never:
        """Getting all entries according to the specified filter."""
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(self, *args: Any, **kwargs: Any) -> Never:
        """Updating a single entry by its ID."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_filter(self, *args: Any, **kwargs: Any) -> Never:
        """Bulk deletion of entries by filter."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_ids(self, *args: Any, **kwargs: Any) -> Never:
        """Bulk deletion of entries by passed IDs."""
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self, *args: Any, **kwargs: Any) -> Never:
        """Bulk delete all entries."""
        raise NotImplementedError
