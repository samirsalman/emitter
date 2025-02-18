from src.events import EventCallback, event
from src.events.events import describe_event


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


def test_event_decorator():
    assert describe_event("count_loop") is not None
    assert describe_event("print_hello_n_times") is not None


def test_event_execution():
    assert count_loop(0, 5) is True
    assert print_hello_n_times(3) is True
