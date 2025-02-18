import asyncio

import pytest

from src.emitters.emitters import AsyncEmitter, DebugEmitter, SyncEmitter
from src.events import EventCallback, event


class BeforeExample(EventCallback):
    def _run(self):
        return True


class AfterExample(EventCallback):
    def _run(self):
        return True


@event(BeforeExample(), AfterExample())
def count_loop(start: int, end: int):
    for i in range(start, end):
        pass
    return True


@event
def print_hello_n_times(n: int):
    for i in range(n):
        pass
    return True


def test_sync_emitter():
    emitter = SyncEmitter()
    emitter.emit("print_hello_n_times", 3)
    assert len(emitter.events) == 1


@pytest.mark.asyncio
def test_async_emitter():
    emitter = AsyncEmitter()
    asyncio.run(emitter.async_emit("print_hello_n_times", 3))
    assert len(emitter.events) == 1


def test_debug_emitter():
    emitter = DebugEmitter()
    emitter.emit("print_hello_n_times", 3)
    assert len(emitter.events) == 1
