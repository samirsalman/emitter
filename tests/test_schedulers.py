import asyncio

import pytest

from src.schedulers.schedulers import Scheduler


def test_scheduler():
    scheduler = Scheduler()
    event_id = scheduler.schedule(lambda: print("Hello"), delay=1)
    assert event_id is not None
    scheduler.cancel(event_id)


@pytest.mark.asyncio
async def test_async_scheduled_event():
    scheduler = Scheduler()
    event_id = scheduler.schedule(lambda: print("Hello"), delay=1)
    await asyncio.sleep(2)
    scheduler.cancel(event_id)
