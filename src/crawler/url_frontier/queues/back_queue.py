from crawler.model.models import URLRecord
from multiprocessing import Queue, Lock, get_logger
import random


class URLBackQueue:
    """
    Esta classe é responsável por gerenciar as filas de URLs de cada domínio.
    TODO:
        - Implementar método dump_to_db() para salvar o mapeamento no banco de dados
          em caso de falha crítica.
        - Implementar método load_from_db() para carregar o mapeamento no banco de dados.
    """

    def __init__(self):
        self.__LOCK__ = Lock()
        self.domain_queues: dict[int, Queue] = dict()
        self.url_count = 0
        self.logger = get_logger()
        self.logger.info('Inicializado.')

    def get_lock(self) -> Lock:
        return self.__LOCK__

    def push(self, url_record: URLRecord) -> None:
        q = url_record['domain_queue']
        if q not in self.domain_queues:
            # Adiciona fila para o domínio
            self.domain_queues[q] = Queue()

        # Adiciona URL na fila correspondente ao domínio
        self.domain_queues[q].put(url_record)
        self.url_count += 1

    def pop(self, domain_queue: int) -> URLRecord | None:
        if self.is_empty():
            return None
        if domain_queue not in self.domain_queues.keys():
            return None

        # Remove URL da fila correspondente ao domínio requisitado
        url_record = self.domain_queues[domain_queue].get()
        self.url_count -= 1

        return url_record

    def random_pop(self) -> URLRecord | None:
        if self.url_count == 0:
            return None

        # Coleta números das filas que não estão vazias
        nonempty_qnums = [qn for qn in self.domain_queues.keys() if not self.domain_queues[qn].empty()]

        # Escolhe uma fila aleatória
        random_qnum = random.sample(nonempty_qnums, 1)[0]

        # Remove URL da fila escolhida
        url_record = self.domain_queues[random_qnum].get()
        self.url_count -= 1

        return url_record

    def is_empty(self) -> int:
        return self.url_count == 0

