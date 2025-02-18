from abc import ABC
import asyncio
import logging

from src.emitters.emitters import AsyncEmitter, BaseEmitter, SyncEmitter, DebugEmitter
from src.events.events import EventDescriptor
from src.schedulers.schedulers import Scheduler
from src.utils.logging import add_log_file, set_level

logger = logging.getLogger(__name__)


class FlowManager:
    def __init__(
        self,
        emitter: BaseEmitter,
        log_level: int = logging.INFO,
        log_file: bool = False,
        log_file_prefix: str = None,
    ):
        self._emitter = emitter
        self._log_level = log_level
        self._log_file = log_file
        self.scheduler = Scheduler()

        set_level(level=self._log_level)

        if self._log_file:
            add_log_file(
                level=self._log_level,
                file_prefix=log_file_prefix,
                dirpath="logs",
            )

    @property
    def emitter(self):
        return self._emitter

    @property
    def events(self) -> list[EventDescriptor]:
        return self.emitter.events

    @classmethod
    def create(cls, emitter: BaseEmitter = None, debug: bool = False):
        if debug:
            emitter = emitter or DebugEmitter()
        else:
            emitter = emitter or SyncEmitter()

        return cls(emitter)

    def emit(self, name: str, *args, **kwargs):
        logger.info(f"Emitting: {name}")
        if isinstance(self.emitter, AsyncEmitter):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.emitter.async_emit(name, *args, **kwargs))
                else:
                    asyncio.run(self.emitter.async_emit(name, *args, **kwargs))
            except RuntimeError:
                asyncio.run(self.emitter.async_emit(name, *args, **kwargs))
        else:
            self.emitter.emit(name, *args, **kwargs)
        logger.info(f"Events: {self.emitter.events}")

    def schedule_emit(self, name: str, *args, delay=0, interval=None, **kwargs):
        """
        Schedule an event to be emitted after a delay.
        If 'interval' is provided, the event is emitted periodically.

        Parameters:
          - name: The event name.
          - *args, **kwargs: Arguments passed to the event handler.
          - delay: Seconds to wait before emitting the event.
          - interval: If provided, the event is re-emitted every `interval` seconds.

        Returns:
          - A unique scheduler ID for the scheduled event.
        """

        def _emit():
            self.emit(name, *args, **kwargs)

        return self.scheduler.schedule(_emit, delay=delay, interval=interval)

    def cancel_scheduled_emit(self, scheduled_id):
        """
        Cancel a scheduled event using its unique scheduler ID.
        """
        self.scheduler.cancel(scheduled_id)

    def on_error(self, e):
        logger.error(f"Error: {e}")
