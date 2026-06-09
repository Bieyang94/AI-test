import threading

_counter_lock = threading.Lock()
_current = 0


def next_num() -> int:
    global _current
    with _counter_lock:
        _current += 1
        return _current


def reset():
    global _current
    with _counter_lock:
        _current = 0
