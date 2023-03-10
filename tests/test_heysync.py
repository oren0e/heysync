import pytest

from heysync import async_to_sync_func, make_sync_class


async def async_func() -> str:
    return "Hey there"


def sync_func() -> str:
    return "I am sync"


class Foo:
    def __init__(self, x: int) -> None:
        self.x = x

    async def __aenter__(self):
        self.x += 2
        await async_func()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        self.x -= 1
        await async_func()

    async def my_func(self) -> str:
        return f"Output is {self.x}"


def test_async_to_sync_func() -> None:
    sync_func1 = async_to_sync_func(async_func)
    result = sync_func1()
    assert result == "Hey there"


def test_async_to_sync_class() -> None:
    FooSync = make_sync_class(Foo)
    foo = FooSync(5)
    result = foo.my_func()  # pylint: disable=no-member
    assert result == "Output is 5"


def test_async_to_sync_class_context() -> None:
    FooSync = make_sync_class(Foo)
    assert FooSync.__name__ == "FooSync"
    with FooSync(7) as foo:  # pylint: disable=not-context-manager
        result = foo.my_func()
        assert result == "Output is 9"
    result = foo.my_func()
    assert result == "Output is 8"


def test_sync_to_sync_err() -> None:
    with pytest.raises(TypeError, match="Function sync_func is not async function"):
        async_to_sync_func(sync_func)


def test_decorator() -> None:
    @async_to_sync_func
    async def some_func() -> str:
        return "boo"

    result = some_func()
    assert result == "boo"
