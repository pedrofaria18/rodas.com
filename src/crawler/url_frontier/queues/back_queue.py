from crawler.model.models import URLRecord
from collections import deque
import logging
import random


class URLBackQueue:
    """
    Esta classe é responsável por gerenciar as filas de URLs de cada domínio.
    TODO:
        - Implementar método dump_to_db() para salvar o mapeamento no banco de dados
          em caso de falha crítica.
        - Implementar método load_from_db() para carregar o mapeamento no banco de dados.
    """

    def __init__(self, handler: logging.FileHandler):
        self.domain_queues: dict[int, deque] = dict()
        self.url_count = 0

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info('Iniciada.')

    def push(self, url_record: URLRecord) -> None:
        q = url_record['domain_queue']
        if q not in self.domain_queues:
            # Adiciona fila para o domínio
            self.domain_queues[q] = deque()

        # Adiciona URL na fila correspondente ao domínio
        self.domain_queues[q].append(url_record)
        self.url_count += 1

    def pop(self, domain_queue: int) -> URLRecord | None:
        if self.is_empty():
            return None
        if domain_queue not in self.domain_queues.keys():
            return None
        # Remove URL da fila correspondente ao domínio requisitado
        url_record = self.domain_queues[domain_queue].popleft()
        self.url_count -= 1
        return url_record

    def random_pop(self) -> URLRecord | None:
        if self.is_empty():
            return None

        # Coleta números das filas que não estão vazias
        nonempty_qnums = [qn for qn in self.domain_queues.keys() if len(self.domain_queues[qn]) > 0]

        # Escolhe uma fila aleatória
        random_qnum = random.sample(nonempty_qnums, 1)[0]

        # Remove URL da fila escolhida
        url_record = self.domain_queues[random_qnum].popleft()
        self.url_count -= 1
        return url_record

    def is_empty(self) -> int:
        return self.url_count == 0
