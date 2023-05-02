from multiprocessing import Lock
from datetime import datetime
import heapq


class URLDownloadQueue:
    """
    Fila de prioridade baseada em heapq.
    """

    def __init__(self):
        self._queue = []
        self._lock = Lock()

    def __len__(self):
        with self._lock:
            return len(self._queue)

    def __contains__(self, url: str):
        with self._lock:
            return url in self._queue

    def push(self, url: str, priority: datetime):
        """Adiciona item na fila com prioridade."""
        with self._lock:
            heapq.heappush(self._queue, (priority, url))

    def pop(self):
        """Remove e retorna o item com a menor prioridade."""
        with self._lock:
            return heapq.heappop(self._queue)[1]

    def peek(self):
        """Retorna o item com a menor prioridade sem removê-lo."""
        with self._lock:
            return self._queue[0][1]

    def is_empty(self):
        """Retorna True se a fila estiver vazia."""
        with self._lock:
            return len(self._queue) == 0

    def clear(self):
        """Esvazia a fila de prioridade."""
        with self._lock:
            self._queue = []
