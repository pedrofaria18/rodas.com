
from src.crawler.url_frontier.front_queue import URLFrontQueue
from multiprocessing import Queue, Lock, get_logger
from urllib.parse import urlparse
import random


class URLBackQueue:
    """
    Esta classe é responsável por gerenciar as filas de URLs de cada domínio.
    """

    __LOG_MAX_URL_SIZE = 30

    def __init__(self):
        self.domain_queues: dict[int, Queue] = dict()
        self.url_count = 0
        self.lock = Lock()
        self.logger = get_logger()

    @staticmethod
    def __trim_url(url: str) -> str:
        return url[:30] + "..." if len(url) > 30 else url

    def push(self, url: str, domain_queue: int) -> None:
        with self.lock:
            if domain_queue not in self.domain_queues:
                # Adiciona fila para o domínio
                self.domain_queues[domain_queue] = Queue()

            # Adiciona URL na fila correspondente ao domínio
            self.domain_queues[domain_queue].put(url)
            self.url_count += 1
            self.logger.info(f"BackQueue: URL {self.__trim_url(url)} added to queue {domain_queue}")

    def pop(self, domain_queue: int) -> str or None:
        with self.lock:
            if self.url_count == 0:
                return None
            if domain_queue not in self.domain_queues.keys():
                return None

            # Remove URL da fila correspondente ao domínio requisitado
            url = self.domain_queues[domain_queue].get()
            self.url_count -= 1

            self.logger.info(f"BackQueue: URL {self.__trim_url(url)} removed from queue {domain_queue}")
            return url

    def random_pop(self) -> str or None:
        with self.lock:
            if self.url_count == 0:
                return None

            # Coleta números das filas que não estão vazias
            nonempty_qnums = [qn for qn in self.domain_queues.keys() if not self.domain_queues[qn].empty()]

            # Escolhe uma fila aleatória
            random_qnum = random.sample(nonempty_qnums, 1)[0]

            # Remove URL da fila escolhida
            url = self.domain_queues[random_qnum].get()
            self.url_count -= 1

            self.logger.info(f"BackQueue: URL {self.__trim_url(url)} removed from queue {random_qnum}")
            return url

    def size(self) -> int:
        with self.lock:
            return self.url_count


class DomainToQueueTable:
    """
    Esta classe é responsável por mapear cada domínio para uma fila de URLs.
    """

    def __init__(self):
        self.domain_to_queue_table = dict()
        self.lock = Lock()
        self.logger = get_logger()

    def log_info(self, domain: str, queue_num: int) -> None:
        self.logger.info(f"DomainToQueueTable: Domain {domain} mapped to queue {queue_num}")

    def get_queue_num(self, domain) -> int:
        with self.lock:
            domain_key = hash(domain)
            if domain_key not in self.domain_to_queue_table:
                queue_num = len(self.domain_to_queue_table)
                self.domain_to_queue_table[domain_key] = queue_num
                self.log_info(domain, queue_num)

            return self.domain_to_queue_table[domain_key]


class FrontToBackQueueRouter:
    """
    Esta classe é responsável por rotear URLs da fila do Front para a fila do Back.
    """

    def __init__(self, front: URLFrontQueue, back: URLBackQueue, domain_to_queue: DomainToQueueTable):
        self.front_queue = front
        self.back_queue = back
        self.domain_to_queue = domain_to_queue
        self.logger = get_logger()

    def run(self):
        while True:
            if self.front_queue.size() > 0:
                # Coleta URL da fila do Front
                url = self.front_queue.pop()

                # Coleta fila do Back correspondente ao domínio da URL
                domain = urlparse(url).netloc
                qnum = self.domain_to_queue.get_queue_num(domain)

                self.back_queue.push(url, qnum)

                trimmed_url = url[:50] + "..." if len(url) > 50 else url
                self.logger.info(f"FrontToBackQueueRouter: URL {trimmed_url} routed to queue {qnum}")
