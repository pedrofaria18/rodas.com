
from crawler.url_frontier.queues.back_queue import URLBackQueue
from crawler.url_frontier.queues.domain_to_queue_table import DomainToQueueTable
from crawler.url_frontier.queues.front_queue import URLFrontQueue
from crawler.logging.log_treatment import url_trimmer

import threading
import logging


class FrontToBackQueueRouter:
    """
    Esta classe é responsável por rotear URLs da fila do Front para a fila do Back.
    TODO:
        - Implementar método dump_to_db() para salvar as filas em um banco de dados
          em caso de falha crítica.
        - Implementar método load_from_db() para carregar as filas no banco de dados.
    """
    def __init__(self, handler: logging.FileHandler):
        self.domain_to_queue = DomainToQueueTable(handler)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info(f'Iniciado.')

    def run(self,
            front_cond:  threading.Condition,
            front_queue: URLFrontQueue,
            back_cond:   threading.Condition,
            back_queue:  URLBackQueue):
        """
        Executa o roteamento de URLs.
        :param front_cond: Condicionador da fila do Front.
        :param front_queue: Fila de Prioridades das URLs a serem visitadas.
        :param back_cond: Condicionador da fila do Back.
        :param back_queue: Fila de Domínios das URLs a serem baixadas.
        """

        self.logger.info(f'Iniciando roteamento de URLs.')

        while True:
            # Coleta URL da fila do Front
            front_cond.acquire()
            while True:
                if not front_queue.is_empty():
                    url_record = front_queue.pop()
                    break
                self.logger.info(f'Fila do Front vazia. Aguardando...')
                front_cond.wait()
            front_cond.release()

            # Coleta fila do Back correspondente ao domínio da URL
            url_record["domain_queue"] = self.domain_to_queue.get_queue_num(url_record['domain_hash'])

            back_cond.acquire()
            back_queue.push(url_record)
            back_cond.notify()
            back_cond.release()
