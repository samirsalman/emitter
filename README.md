# Emitter 🚀

**Emitter** is a lightweight, event-driven Python library designed to simplify the management of execution flows. By leveraging event callbacks and decorators, Emitter makes it easy to attach pre- and post-execution logic to your functions—ideal for logging, instrumentation, or any cross-cutting concerns.

## Features ✨

- **Event-Based Architecture**  
  Easily attach events to functions using the `@event` decorator.
- **Synchronous & Asynchronous Support**  
  Choose between `SyncEmitter` and `AsyncEmitter` to fit your workflow needs.
- **Flow Management**  
  Organize and manage complex workflows with the `FlowManager`.
- **Customizable Callbacks**  
  Define your own before/after hooks by extending `EventCallback`.
- **Integrated Logging**  
  Optionally log event flows to a file with customizable settings.

## Installation

Clone the repository and navigate to its directory:

```bash
git clone https://github.com/samirsalman/emitter.git
cd emitter
```

> **Note:** This project requires Python 3.6 or higher. Install any additional dependencies as needed.

## Usage

Emitter makes it simple to decorate functions with events. For example:

```python
import logging
import time
import random
from emitter import event, EventCallback
from emitter import FlowManager, SyncEmitter

# Define custom event callbacks
class BeforeExample(EventCallback):
    def _run(self):
        print("Before Example")
        return True

class AfterExample(EventCallback):
    def _run(self):
        print("After Example")
        return True

# Decorate functions to attach events
@event(BeforeExample(), AfterExample())
def count_loop(start: int, end: int):
    for i in range(start, end):
        print(i)
        time.sleep(random.random())
    return True

@event(BeforeExample(), AfterExample())
def console():
    print("Hello, World!")
    return True

@event
def print_hello_n_times(n: int):
    for i in range(n):
        print("Hello")
        time.sleep(random.random())
    return True

# Example flow execution using FlowManager
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
```

Check out the [`main.py`](https://github.com/samirsalman/emitter/blob/main/main.py) file for a complete working example.

## Contributing

Contributions are welcome! If you have ideas for improvements, encounter any issues, or want to add new features, please feel free to open an issue or submit a pull request.

## Contact

For inquiries or further information, please visit the [GitHub profile of samirsalman](https://github.com/samirsalman).
