from __future__ import annotations

import typing
from typing import Awaitable, Callable, ParamSpec, TypeVar

import anyio
import anyio.abc

Args = typing.TypeVarTuple("Args")
T = typing.TypeVar("T")
U = typing.TypeVar("U")


class FutureFinishedWithExceptionError(Exception):
    """An error raised when a future finished with an exception."""


class FutureNotSetError(Exception):
    """An error raised when a future is not set."""


class SimpleFuture[T]:
    """A simple anyio-based future.

    Futures can hold a single result, which is provided by an async task. Following anyio (rather
    than asyncio) conventions, every task is associated with a task group. Futures allow us to
    more easily pass around "boxes" that will eventually contain results.

    Note that if you just want to wait for a set of tasks to complete, you can just use an anyio
    task group, and store the result in a mutable container like a list or dict; you don't need
    futures the same way you do in asyncio. This class is most useful when either:
    - you only have a single result of each type and don't want to deal with creating a list with
      one element, or want the more convenient typechecked interface of SimpleFuture,
    - you want to pass a box between two tasks, so that one task can set the result and another
      can wait for it to be set, without requiring a more heavyweight mechanism like a queue.

    A basic low-level pattern you can use to run a task and get its result later:

    ```python
    async with anyio.create_task_group() as tg:
        future = SimpleFuture()

        async def go(*args):
            future.set_result(await some_task_fn(*args))

        tg.start_soon(go, *args)

        # do something else asynchronously while the task runs

    # once you exit the task group, the future will have a result
    value = future.get()
    ```

    This pattern is useful enough that there is a wrapper so that you can instead do:

    ```python
    async with anyio.create_task_group() as tg:
        future = future_from_start_soon(tg, some_task_fn, *args)
        # do something else asynchronously while the task runs

    # once you exit the task group, the future will have a result
    value = future.get()
    ```

    You can also use `await future.wait_for_result()` to wait for the future to complete and get
    the result.
    """

    def __init__(self):
        self.event = anyio.Event()
        self.result = None
        self.exception = None

    def set_result(self, result: T):
        """Set the result of the future."""

        assert not self.event.is_set(), "Result already set"
        self.result = result
        self.event.set()

    def set_from_task(
        self,
        task_fn: Callable[[*Args], typing.Awaitable[T]],
        set_exception: bool = True,
        catch_exception: bool = False,
    ) -> Callable[[*Args], typing.Awaitable[None]]:
        """Wrap a callable to set the result of the future from its result.

        This function can be used to wrap a task that returns a value into a task that sets a
        future. It is most useful in combination with `TaskGroup.start_soon`, e.g.

        ```python
        future = SimpleFuture()
        async with anyio.create_task_group() as tg:
            # runs `await some_task_fn(*args)` and sets the future to the result
            tg.start_soon(future.set_from_task(some_task_fn), *args)

            # or, same pattern but with keyword arguments
            tg.start_soon(future.set_from_task(functools.partial(some_task_fn, **kwargs)))
        ```

        Args:
            task_fn: A callable that returns an awaitable.
            set_exception: Whether to set the future to the exception if the task raises an
                exception. If False, the exception will not be set.
            catch_exception: Whether to catch exceptions and set the future to the exception. If
                False (the default), exceptions will be propagated up to the task group. If True,
                exceptions will be caught and will not cancel the task group. `set_exception` must
                be True if `catch_exception` is True.

        Returns:
            A callable that can be used to start a task that sets the future to the result of
            `task_fn`.
        """
        if catch_exception and not set_exception:
            raise ValueError("set_exception must be True if catch_exception is True")

        async def wrapped_task_fn(*args: *Args):
            try:
                result = await task_fn(*args)
            except Exception as e:
                if set_exception:
                    self.set_exception(e)
                    if not catch_exception:
                        raise
                else:
                    raise
            else:
                self.set_result(result)

        return wrapped_task_fn

    def set_exception(self, exception: Exception):
        """Set the result of the future to an exception."""
        assert not self.event.is_set(), "Result already set"
        self.exception = exception
        self.event.set()

    def has_result(self) -> bool:
        """Check if the future has a result."""
        return self.event.is_set()

    async def wait_for_result(self) -> T:
        """Wait for the future to complete and return the result.

        If the future has an exception, it will be raised.
        """
        await self.event.wait()
        if self.exception:
            raise FutureFinishedWithExceptionError(
                f"Future finished with an exception (of type {type(self.exception).__name__})!"
            ) from self.exception
        assert self.result is not None
        return self.result

    def get(self) -> T:
        """Synchronously get the result of the future.

        If the future has an exception, it will be raised.
        """
        if not self.has_result():
            raise FutureNotSetError("Result not set")
        if self.exception:
            raise self.exception
        assert self.result is not None
        return self.result


def future_from_start_soon[
    T, *Args
](
    task_group: anyio.abc.TaskGroup,
    task_fn: Callable[[*Args], Awaitable[T]],
    *args: *Args,
    catch_exception: bool = False,
) -> SimpleFuture[T]:
    """Create a future from the result of starting a coroutine in a task group.

    This is a convenience function for creating a future and starting a task in a task group.
    It can be used like this:

    ```python
    async with anyio.create_task_group() as tg:
        future = future_from_start_soon(tg, some_task_fn, *args)
    ```

    Args:
        task_group: The task group to start the task in. This is the task group that owns the
            task and will be cancelled if the task raises an exception (unless
            `catch_exception` is True).
        task_fn: The coroutine to start.
        *args: The arguments to pass to the coroutine.
        catch_exception: Whether to catch exceptions and set the future to the exception. If
            False (the default), exceptions will be propagated up to the task group. If True,
            exceptions will be caught and stored in the future instead, and the task group
            will not be cancelled.

    Returns:
        A future that will eventually contain the result of the coroutine, or an exception if
        the coroutine raises an exception and `catch_exception` is True.
    """
    result = SimpleFuture[T]()
    task_group.start_soon(
        result.set_from_task(task_fn, set_exception=True, catch_exception=catch_exception),
        *args,
    )
    return result


P = ParamSpec("P")  # full parameter list of the wrapped function
T = TypeVar("T")  # its return type

