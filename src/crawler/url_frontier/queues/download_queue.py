from multiprocessing import Lock, get_logger
from datetime import datetime
import heapq

from crawler.model.models import URLRecord


class URLDownloadQueue:
    """
    Fila de prioridade baseada em heapq.
    """

    def __init__(self):
        self.__lock__ = Lock()
        self.queue = []
        self.logger = get_logger()
        self.logger.info('Inicializado.')

    def __len__(self) -> int:
        return len(self.queue)

    def __contains__(self, url_record: str) -> bool:
        return url_record in self.queue

    def get_lock(self) -> Lock:
        return self.__lock__

    def push(self, url_record: URLRecord, priority: datetime) -> None:
        """Adiciona item na fila com prioridade."""
        heapq.heappush(self.queue, (priority, url_record))

    def pop(self) -> URLRecord:
        """Remove e retorna o item com a menor prioridade."""
        return heapq.heappop(self.queue)[1]

    def peek(self) -> URLRecord:
        """Retorna o item com a menor prioridade sem removê-lo."""
        return self.queue[0][1]

    def is_empty(self) -> bool:
        """Retorna True se a fila estiver vazia."""
        return len(self.queue) == 0

    def clear(self) -> None:
        """Esvazia a fila de prioridade."""
        self.queue = []
