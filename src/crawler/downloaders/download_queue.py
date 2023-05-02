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
        return len(self._queue)

    def __contains__(self, url: str):
        return url in self._queue

    def push(self, url: str, priority: datetime):
        """Adiciona item na fila com prioridade."""
        heapq.heappush(self._queue, (priority, url))

    def pop(self):
        """Remove e retorna o item com a menor prioridade."""
        return heapq.heappop(self._queue)[1]

    def peek(self):
        """Retorna o item com a menor prioridade sem removê-lo."""
        return self._queue[0][1]

    def is_empty(self):
        """Retorna True se a fila estiver vazia."""
        return len(self._queue) == 0

    def clear(self):
        """Esvazia a fila de prioridade."""
        self._queue = []
