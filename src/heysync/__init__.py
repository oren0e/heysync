import asyncio
from functools import wraps
from typing import Callable

from heysync.utils import get_or_create_eventloop


def async_to_sync_func(func: Callable):
    """
    Function to convert async function into sync function
    """
    if not asyncio.iscoroutinefunction(func):
        raise TypeError(f"Function {func.__name__} is not async function")

    @wraps(func)
    def run(*args, **kwargs):
        coroutine = func(*args, **kwargs)
        loop = get_or_create_eventloop()
        if loop.is_running():
            return coroutine
        return loop.run_until_complete(coroutine)

    return run


def make_sync_class(async_class):
    """
    Return a sync version of a class that has async methods
    """
    name_map = {
        "__aenter__": "__enter__",
        "__aexit__": "__exit__",
    }
    new_members = {}
    members = async_class.__dict__
    for name, value in members.items():
        if asyncio.iscoroutinefunction(value):
            new_name = name_map.get(name, name)
            new_members[new_name] = async_to_sync_func(value)
        else:
            new_members[name] = value
    return type(async_class.__name__ + "Sync", async_class.__bases__, new_members)
