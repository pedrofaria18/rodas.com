from crawler.url_frontier.queues.back_queue import URLBackQueue
from crawler.url_frontier.queues.domain_to_queue_table import DomainToQueueTable
from crawler.url_frontier.queues.front_queue import URLFrontQueue
from crawler.logging.machinery import url_trimmer
from multiprocessing import get_logger


class FrontToBackQueueRouter:
    """
    Esta classe é responsável por rotear URLs da fila do Front para a fila do Back.
    TODO:
        - Implementar método dump_to_db() para salvar as filas em um banco de dados
          em caso de falha crítica.
        - Implementar método load_from_db() para carregar as filas no banco de dados.
    """
    domain_to_queue = DomainToQueueTable()

    def __init__(self, front_queue: URLFrontQueue, back_queue: URLBackQueue):
        self.front_queue = front_queue
        self.__FRONT_LOCK__ = front_queue.get_lock()
        self.back_queue = back_queue
        self.__BACK_LOCK__ = back_queue.get_lock()
        self.logger = get_logger()
        self.logger.info('Inicializado.')

    def run(self):
        while True:
            # Coleta URL da fila do Front
            with self.__FRONT_LOCK__:
                if self.front_queue.is_empty():
                    continue
                url_record = self.front_queue.pop()

            # Coleta fila do Back correspondente ao domínio da URL
            url_record["domain_queue"] = self.domain_to_queue.get_queue_num(url_record['domain_hash'])

            with self.__BACK_LOCK__:
                self.back_queue.push(url_record)

            self.logger.info(f'URL {url_trimmer(url_record["url"])} roteada para '
                             f'fila [Back {url_record["domain_queue"]}].')
