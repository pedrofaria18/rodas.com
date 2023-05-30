from crawler.model.models import URLRecord
from datetime import datetime
import heapq
import logging


class URLDownloadQueue:
    """
    Fila de prioridade baseada em heapq.
    """

    def __init__(self, handler: logging.FileHandler):
        self.queue = []

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info('Iniciada.')

    def __len__(self) -> int:
        return len(self.queue)

    def __contains__(self, url_record: str) -> bool:
        return url_record in self.queue

    def push(self, url_record: URLRecord, priority: datetime) -> None:
        """Adiciona item na fila com prioridade."""
        heapq.heappush(self.queue, (priority, len(self.queue), url_record))

    def pop(self) -> URLRecord:
        """Remove e retorna o item com a menor prioridade."""
        return heapq.heappop(self.queue)[2]

    def peek(self) -> URLRecord:
        """Retorna o item com a menor prioridade sem removê-lo."""
        return self.queue[0][2]

    def is_empty(self) -> bool:
        """Retorna True se a fila estiver vazia."""
        return len(self.queue) == 0

    def clear(self) -> None:
        """Esvazia a fila de prioridade."""
        self.queue = []
