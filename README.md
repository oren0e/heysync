# Hey, Sync!

This package will allow you to convert an async function or a class (that has async methods) to a sync version.  
The new class name will be set as `<OLD CLASS NAME>Sync`

## Installation

`pip install heysync`

## Usage

### Async Functions

You can convert async functions to sync function by:

1. Normal usage:

```python
from heysync import async_to_sync_func

async def async_func() -> str:
    return "Hey there"

sync_func = async_to_sync_func(async_func)

# now you can call sync_func in the usual way
sync_func()  # Hey there
```

2. As a decorator:

```python
from heysync import async_to_sync_func

@async_to_sync_func
async def some_func() -> str:
    return "boo"

some_func()  # boo
```

### Classes

You can also convert async classes:

```python
from heysync import make_sync_class

# a class with async methods
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

FooSync = make_sync_class(Foo)
with Foo(7) as foo:
    foo.my_func()  # Output is 9
foo.my_func()  # Output is 8
```
