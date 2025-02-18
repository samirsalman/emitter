import asyncio
import logging
import threading
import uuid

logger = logging.getLogger(__name__)


class AsyncScheduledEvent:
    def __init__(self, func, delay=0, interval=None, *args, loop=None, **kwargs):
        """
        Parameters:
          - func: The function to execute (sync or async).
          - delay: Seconds to wait before first execution.
          - interval: If provided, re-execute every `interval` seconds.
          - loop: The asyncio event loop to run the event on.
          - *args, **kwargs: Arguments passed to the function.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.delay = delay
        self.interval = interval
        self.loop = loop  # Required event loop (background loop)
        self.future = None
        self.id = uuid.uuid4().hex

    async def _run(self):
        try:
            await asyncio.sleep(self.delay)
            if self.interval is None:
                await self._call_func()
            else:
                while True:
                    await self._call_func()
                    await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            logger.info(f"Scheduled event {self.id} cancelled")
            raise

    async def _call_func(self):
        if asyncio.iscoroutinefunction(self.func):
            await self.func(*self.args, **self.kwargs)
        else:
            # Run synchronous function in an executor to avoid blocking.
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.func, *self.args, **self.kwargs)

    def start(self):
        if self.loop is None:
            raise RuntimeError("No event loop available for scheduled event")
        # Schedule the coroutine on the provided loop from a different thread.
        self.future = asyncio.run_coroutine_threadsafe(self._run(), self.loop)

    def cancel(self):
        if self.future:
            self.future.cancel()


class Scheduler:
    def __init__(self):
        self.scheduled_events = {}
        # Create a dedicated event loop running in a background thread.
        self._loop = asyncio.new_event_loop()
        t = threading.Thread(target=self._start_loop, daemon=True)
        t.start()

    def _start_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def schedule(self, func, delay=0, interval=None, *args, **kwargs):
        """
        Schedule a function (sync or async) to run after a delay,
        optionally repeating every `interval` seconds.

        Returns:
          - A unique event ID for cancellation.
        """
        event = AsyncScheduledEvent(
            func, delay, interval, *args, loop=self._loop, **kwargs
        )
        self.scheduled_events[event.id] = event
        event.start()
        return event.id

    def cancel(self, event_id):
        """
        Cancel a scheduled event by its unique ID.
        """
        event = self.scheduled_events.get(event_id)
        if event:
            event.cancel()
            del self.scheduled_events[event_id]
