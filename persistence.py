from typing import Any, Dict, Optional
import json
import threading
import os

class InMemorySaver:
    """Thread-level checkpoint storage. Not durable across process restarts.

    Used by the workflow for fast, in-memory checkpointing within a process or thread.
    """
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def save(self, key: str, value: Any) -> None:
        with self._lock:
            self._store[key] = value

    def load(self, key: str) -> Optional[Any]:
        with self._lock:
            return self._store.get(key)


class InMemoryStore:
    """Simple long-term store for lightweight facts (in-memory).

    This is separate from conversation history and intended for small cross-session
    facts like a user's budget goal or preferred currency.
    """
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._lock = threading.Lock()

    def save(self, key: str, value: Any) -> None:
        with self._lock:
            self._store[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._store.get(key, default)


class JSONFileStore(InMemoryStore):
    """Optional simple file-backed store for longer persistence.

    Saves the entire store as JSON to disk on each save call. Not optimized, but
    useful for small demos where you want persistence across process restarts.
    """
    def __init__(self, path: str = "persist_store.json"):
        super().__init__()
        self.path = path
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self._store = data
            except Exception:
                self._store = {}

    def save(self, key: str, value: Any) -> None:
        super().save(key, value)
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._store, f, ensure_ascii=False, indent=2)
        except Exception:
            # best-effort; ignore disk errors in demo code
            pass
