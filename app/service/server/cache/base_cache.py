import time
import threading
from typing import TypeVar, Generic, Optional

V = TypeVar("V")


class BaseCache(Generic[V]):
    def __init__(self, max_entries: int = 100, ttl_seconds: int = 3600):
        self._store: dict[int, tuple[V, float]] = {}
        self._lock = threading.Lock()
        self._max_entries = max_entries
        self._ttl = ttl_seconds

    def get(self, num: int) -> Optional[V]:
        with self._lock:
            entry = self._store.get(num)
            if entry is None:
                return None
            value, ts = entry
            if self._ttl > 0 and (time.time() - ts) > self._ttl:
                self._store.pop(num, None)
                return None
            return value

    def set(self, num: int, value: V) -> None:
        with self._lock:
            if num not in self._store and len(self._store) >= self._max_entries:
                oldest_key = min(self._store, key=lambda k: self._store[k][1])
                self._store.pop(oldest_key)
            self._store[num] = (value, time.time())

    def delete(self, num: int) -> bool:
        with self._lock:
            return self._store.pop(num, None) is not None

    def exists(self, num: int) -> bool:
        return self.get(num) is not None

    def clear_all(self) -> int:
        with self._lock:
            count = len(self._store)
            self._store.clear()
            return count
