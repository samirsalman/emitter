from abc import ABC, abstractmethod


_EVENTS = []


def _clean_args(args, kwds, fn):
    varnames = fn.__code__.co_varnames
    varnames = [
        varname for varname in varnames if varname != "self" and varname != "cls"
    ]

    args = args[: len(varnames)]
    kwds = {k: v for k, v in kwds.items() if k in varnames}
    return args, kwds


class Event(ABC):
    def __init__(
        self,
        name: str,
        callback: callable,
        before: "EventCallback" = None,
        after: "EventCallback" = None,
    ):
        self.name = name
        self.before = before or None
        self.after = after or None
        self.callback = callback

    def __call__(self, *args, **kwds):
        if self.before is not None:
            before_args, before_kwds = _clean_args(args, kwds, self.before._run)
            self.before.run(*before_args, **before_kwds)
        callback_args, callback_kwds = _clean_args(args, kwds, self.callback)
        self.callback(*callback_args, **callback_kwds)
        if self.after is not None:
            after_args, after_kwds = _clean_args(args, kwds, self.after._run)
            self.after.run(*after_args, **after_kwds)


class EventCallback(ABC):
    @abstractmethod
    def _run(self, *args, **kwds):
        pass

    def run(self, *args, **kwds):
        args, kwds = _clean_args(args, kwds, self._run)
        return self._run(*args, **kwds)



def event(before: EventCallback = None, after: EventCallback = None):
    def decorator(callback):
        _EVENTS.append(Event(name=callback.__name__, callback=callback, before=before, after=after))
        return callback

    if callable(before):
        return decorator(before)
    return decorator
