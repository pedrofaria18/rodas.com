from crawler.url_frontier.url_prioritizers.url_prioritizer_default import URLPrioritizer
from crawler.interfaces.i_url_prioritizer import URLPrioritizerInterface
from crawler.model.models import URLRecord
from collections import deque
import logging


class URLFrontQueue:
    """
    Esta classe é responsável por gerenciar as filas do Front de URLs de cada domínio.
    """

    def __init__(self, handler: logging.FileHandler):
        self.prioritizer: URLPrioritizerInterface = URLPrioritizer()
        self.queues: dict[int, deque] = dict()
        self.url_count: int = 0

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info('Iniciada.')

    def push(self, url_record: URLRecord) -> None:
        priority = self.prioritizer.get_priority(url_record)
        if priority not in self.queues:
            self.queues[priority] = deque()

        for record in self.queues[priority]:
            if record['url_hash'] == url_record['url_hash']:
                return

        self.queues[priority].append(url_record)
        self.url_count += 1

    def pop(self) -> URLRecord | None:
        """
        Remove um URLRecord da fila não vazia e de menor valor de prioridade.
        :return: Retorna um URLRecord ou None caso o Front esteja vazio.
        """
        if self.is_empty():
            return None

        priorities = [p for p in self.queues.keys() if len(self.queues[p]) > 0]

        # Política de seleção: menor valor de prioridade
        url_record = self.queues[min(priorities)].popleft()
        self.url_count -= 1
        return url_record

    def is_empty(self) -> bool:
        return self.url_count == 0
