import asyncio
from dataclasses import dataclass

from emitter.events import _EVENTS, Event


def emit(name: str, *args, **kwds):
    for event in _EVENTS:
        if event.name == name:
            event(*args, **kwds)
            break


async def async_emit(name: str, *args, **kwds):
    for event in _EVENTS:
        if event.name == name:
            if asyncio.iscoroutinefunction(event.__call__):
                await event(*args, **kwds)
            else:
                event(*args, **kwds)
            break

    return True


@dataclass
class EventDescriptor:
    event: Event

    def __repr__(self):
        return f"Event(name={self.event.name}, before={self.event.before.__class__.__name__}, after={self.event.after.__class__.__name__}, callback={self.event.callback.__name__})"


def describe_event(name: str):
    for event in _EVENTS:
        if event.name == name:
            return EventDescriptor(event)
    return None
