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
            # Check if before has a _run attribute; if not, call it directly.
            if hasattr(self.before, "_run"):
                before_args, before_kwds = _clean_args(args, kwds, self.before._run)
                self.before.run(*before_args, **before_kwds)
            else:
                self.before(*args, **kwds)
        callback_args, callback_kwds = _clean_args(args, kwds, self.callback)
        self.callback(*callback_args, **callback_kwds)
        if self.after is not None:
            if hasattr(self.after, "_run"):
                after_args, after_kwds = _clean_args(args, kwds, self.after._run)
                self.after.run(*after_args, **after_kwds)
            else:
                self.after(*args, **kwds)


class EventCallback(ABC):
    @abstractmethod
    def _run(self, *args, **kwds):
        pass

    def run(self, *args, **kwds):
        args, kwds = _clean_args(args, kwds, self._run)
        return self._run(*args, **kwds)


def _wrap_event_callback(cb):
    """
    If cb does not have a _run attribute, wrap it in a simple EventCallback.
    """
    if cb is None:
        return None
    if hasattr(cb, "_run"):
        return cb  # Already an EventCallback instance.

    # Otherwise, wrap the callable in an EventCallback.
    class WrappedCallback(EventCallback):
        def _run(self, *args, **kwds):
            return cb(*args, **kwds)

    return WrappedCallback()


def event(before: EventCallback = None, after: EventCallback = None):

    if callable(before) and not callable(after):
        callback = before
        before = None
        after = None
        return event()(callback)

    before = _wrap_event_callback(before)
    after = _wrap_event_callback(after)

    def decorator(fn):
        name = fn.__name__
        e = Event(name, fn, before, after)
        _EVENTS.append(e)
        return fn

    return decorator
