import asyncio
import logging
from abc import ABC, abstractmethod

from emitter.events.events import async_emit, describe_event, emit

logger = logging.getLogger(__name__)


class BaseEmitter(ABC):
    def __init__(self, *args, **kwargs):
        self._events = []

    @property
    def events(self):
        return self._events

    def on_error(self, e):
        logger.error(f"Error: {e}")

    @abstractmethod
    def before_emit(self, *args, **kwargs):
        pass

    @abstractmethod
    def after_emit(self, *args, **kwargs):
        pass

    def emit(self, name: str, *args, **kwargs):
        try:
            self.before_emit(*args, **kwargs)
            logger.debug(f"Emitting: {name}")
            emit(name, *args, **kwargs)
            self._events.append(describe_event(name))
            self.after_emit(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error: {e}")
            if self.on_error:
                self.on_error(e)
            else:
                raise e


class AsyncEmitter(BaseEmitter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def executor(self):
        return asyncio.create_task

    async def async_before_emit(self, *args, **kwargs):
        pass

    async def async_after_emit(self, *args, **kwargs):
        pass

    async def async_emit(self, name: str, *args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(self.async_before_emit):
                await self.async_before_emit(*args, **kwargs)
            else:
                self.before_emit(*args, **kwargs)

            if asyncio.iscoroutinefunction(async_emit):
                await async_emit(name, *args, **kwargs)
            else:
                emit(name, *args, **kwargs)

            self._events.append(describe_event(name))
            if asyncio.iscoroutinefunction(self.async_after_emit):
                await self.async_after_emit(*args, **kwargs)
            else:
                self.after_emit(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error: {e}")
            if self.on_error:
                self.on_error(e)
            else:
                raise e

    def before_emit(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.async_before_emit):
            return self.executor(self.async_before_emit(*args, **kwargs))
        return self.async_before_emit(*args, **kwargs)

    def after_emit(self, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.async_after_emit):
            return self.executor(self.async_after_emit(*args, **kwargs))
        return self.async_after_emit(*args, **kwargs)

    def emit(self, name: str, *args, **kwargs):
        if asyncio.iscoroutinefunction(self.async_emit):
            return self.executor(self.async_emit(name, *args, **kwargs))

        return self.async_emit(name, *args, **kwargs)


class SyncEmitter(BaseEmitter):

    def before_emit(self, *args, **kwargs):
        logger.debug("Before Emit")

    def after_emit(self, *args, **kwargs):
        logger.debug("After Emit")


class DebugEmitter(BaseEmitter):

    def before_emit(self, *args, **kwargs):
        logger.debug("Before Emit")

    def after_emit(self, *args, **kwargs):
        logger.debug("After Emit")
