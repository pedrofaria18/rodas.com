from crawler.interfaces.i_url_prioritizer import URLPrioritizerInterface
from crawler.model.models import URLRecord
from multiprocessing import Queue, Lock, get_logger


class URLFrontQueue:
    """
    Esta classe é responsável por gerenciar as filas do Front de URLs de cada domínio.
    """

    def __init__(self, prioritizer: URLPrioritizerInterface):
        self.queues: dict[int, Queue] = dict()
        self.url_count: int = 0
        self.prioritizer = prioritizer
        self.__LOCK__ = Lock()
        self.logger = get_logger()
        self.logger.info('Inicializado.')

    def get_lock(self) -> Lock:
        return self.__LOCK__

    def push(self, url_record: URLRecord) -> None:
        priority = self.prioritizer.get_priority(url_record)
        if priority not in self.queues:
            self.queues[priority] = Queue()

        self.queues[priority].put(url_record)
        self.url_count += 1

    def pop(self) -> URLRecord | None:
        """
        Remove um URLRecord da fila não vazia e de menor valor de prioridade.
        :return: Retorna um URLRecord ou None caso o Front esteja vazio.
        """
        if self.is_empty():
            return None

        priorities = [p for p in self.queues.keys() if not self.queues[p].empty()]

        # Política de seleção: menor valor de prioridade
        url = self.queues[min(priorities)].get()
        self.url_count -= 1
        return url

    def is_empty(self) -> bool:
        return self.url_count == 0
