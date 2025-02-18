import logging
import random
import time
from src.emitters.emitters import SyncEmitter
from src.events import EventCallback, event
from src.emitters import AsyncEmitter
from src.flows.manager import FlowManager


class BeforeExample(EventCallback):
    def _run(self):
        print("Before Example")
        return True


class AfterExample(EventCallback):
    def _run(self):
        print("After Example")
        return True


@event(BeforeExample(), AfterExample())
def count_loop(
    start: int,
    end: int,
):
    for i in range(start, end):
        print(i)
        time.sleep(random.random())

    return True


@event(BeforeExample(), AfterExample())
def console(*args, **kwds):
    print("Hello, World!")
    return True

@event
def print_hello_n_times(
    n: int,
):
    for i in range(n):
        print("Hello")
        time.sleep(random.random())

    return True




if __name__ == "__main__":
    manager = FlowManager(
        emitter=SyncEmitter(),
        log_file=True,
        log_file_prefix="example",
        log_level=logging.DEBUG
    )    

    manager.emit("print_hello_n_times", 5)

    manager.emit("count_loop", 0, 10)
    time.sleep(1)

    manager.emit("console")

    
