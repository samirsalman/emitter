import logging
import time
import random
from src.emitters.emitters import SyncEmitter
from src.events.events import event, EventCallback
from src.flows.manager import FlowManager

# Custom callbacks implementing EventCallback.
class BeforeExample(EventCallback):
    def _run(self):
        print("Before Example")
        return True

class AfterExample(EventCallback):
    def _run(self):
        print("After Example")
        return True

# Attach before/after hooks to the function.
@event(BeforeExample(), AfterExample())
def count_loop(start: int, end: int):
    for i in range(start, end):
        print(i)
        time.sleep(random.random())
    return True

# A simple event with automatically-wrapped callbacks.
@event
def print_hello_n_times(n: int):
    for i in range(n):
        print("Hello")
        time.sleep(random.random())
    return True

if __name__ == "__main__":
    # Create a FlowManager instance using the default (SyncEmitter).
    manager = FlowManager.create()

    # Emit events immediately.
    manager.emit("print_hello_n_times", 3)
    manager.emit("count_loop", 0, 5)

    # Schedule an event to run after 5 seconds.
    scheduler_id = manager.schedule_emit("print_hello_n_times", 2, delay=5)
    print(f"Scheduled 'print_hello_n_times' event with ID: {scheduler_id}")

    # Schedule a periodic event (runs every 4 seconds after an initial 2-second delay).
    periodic_id = manager.schedule_emit("count_loop", 10, 15, delay=2, interval=4)
    print(f"Scheduled periodic 'count_loop' event with ID: {periodic_id}")

    # Let scheduled events run for a while then cancel the periodic event.
    time.sleep(12)
    manager.cancel_scheduled_emit(periodic_id)
    print("Cancelled periodic event.")

    # Allow time for any remaining scheduled events.
    time.sleep(5)