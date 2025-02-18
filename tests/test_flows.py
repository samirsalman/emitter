from emitter.emitters.emitters import AsyncEmitter, DebugEmitter, SyncEmitter
from emitter.flows.manager import FlowManager


def test_flow_manager_sync():
    manager = FlowManager.create(SyncEmitter())
    manager.emit("print_hello_n_times", 3)
    assert len(manager.events) == 1


def test_flow_manager_async():
    manager = FlowManager.create(AsyncEmitter())
    manager.emit("print_hello_n_times", 3)
    assert len(manager.events) == 1


def test_flow_manager_debug():
    manager = FlowManager.create(DebugEmitter())
    manager.emit("print_hello_n_times", 3)
    assert len(manager.events) == 1


def test_schedule_emit():
    manager = FlowManager.create(SyncEmitter())
    scheduler_id = manager.schedule_emit("print_hello_n_times", 2, delay=1)
    assert scheduler_id is not None
    manager.cancel_scheduled_emit(scheduler_id)
