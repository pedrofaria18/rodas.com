from crawler.url_frontier.queues.download_queue import URLDownloadQueue
from crawler.url_frontier.queues.back_queue import URLBackQueue
from crawler.logging.log_treatment import url_trimmer
from datetime import datetime, timedelta

import threading
import logging
import time


class URLDownloadScheduler:
    """
    Esta classe é responsável por agendar o download de URLs.
    :param delay_in_seconds: Tempo de espera entre downloads de um mesmo domínio.

    TODO:
        - Avaliar se vale a pena implementar leitura de `robots.txt` para delays.
        - Implementar salvamento de estado no banco de dados em caso de falha crítica.
    """

    def __init__(self, handler: logging.FileHandler, delay_in_seconds: int = 10):
        self.DELAY_IN_SECONDS = delay_in_seconds
        self.domain_last_visit = dict()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info(f'Iniciado.')

    def _set_domain_last_visit(self, domain_queue: int, last_visit: datetime) -> None:
        """ Define a última visita ao host. """
        self.domain_last_visit[domain_queue] = last_visit

    def _get_domain_next_visit(self) -> (int | None, datetime | None):
        """ Retorna o próximo host a ser visitado. """
        if not self.domain_last_visit:
            return None, None

        min_datetime = min(self.domain_last_visit.values())
        domain_num = next((d for d, lv in self.domain_last_visit.items() if lv == min_datetime), None)
        if domain_num is None:
            return None, None

        next_visit = min_datetime + timedelta(seconds=self.DELAY_IN_SECONDS)
        self._set_domain_last_visit(domain_num, next_visit)

        return domain_num, next_visit

    def run(self,
            back_cond:      threading.Condition,
            back_queue:     URLBackQueue,
            download_cond:  threading.Condition,
            download_queue: URLDownloadQueue):
        """
        Executa o agendamento de downloads.
        :param back_cond: Lock para a fila de URLs a serem visitadas.
        :param back_queue: Fila de URLs a serem visitadas.
        :param download_cond: Lock para a fila de URLs a serem baixadas.
        :param download_queue: Fila de URLs a serem baixadas.
        """

        self.logger.info(f'Iniciando o agendamento de downloads.')

        while True:
            domain_num, next_visit = self._get_domain_next_visit()

            # Fila de URLs
            back_cond.acquire()
            while True:
                if not back_queue.is_empty():
                    time.sleep(self.DELAY_IN_SECONDS)
                    if domain_num:
                        url_record = back_queue.pop(domain_num)
                        next_visit += timedelta(seconds=self.DELAY_IN_SECONDS)
                    else:
                        url_record = back_queue.random_pop()
                        next_visit = datetime.now()
                    break
                self.logger.info(f'Fila de URLs vazia. Aguardando...')
                back_cond.wait()
            back_cond.release()

            # Fila de downloads
            download_cond.acquire()
            self._set_domain_last_visit(url_record['domain_queue'], next_visit)
            download_queue.push(url_record, next_visit)
            download_cond.notify()
            download_cond.release()

            self.logger.debug(f'Download agendado para {next_visit}, URL: {url_trimmer(url_record["url"])}.')
