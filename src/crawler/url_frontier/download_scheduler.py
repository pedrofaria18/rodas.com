from crawler.url_frontier.queues.download_queue import URLDownloadQueue
from crawler.url_frontier.queues.back_queue import URLBackQueue
from crawler.logging.log_treatment import url_trimmer
from datetime import datetime, timedelta

import threading
import logging


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

    def _get_domain_next_visit(self) -> (int | None, datetime | None):
        """ Retorna o próximo host a ser visitado. """
        if len(self.domain_last_visit) == 0:
            return None, None

        min_datetime = min(self.domain_last_visit.values())
        domain_num = [k for k, v in self.domain_last_visit.items() if v == min_datetime][0]

        return domain_num, min_datetime

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
                    if domain_num:
                        url_record = back_queue.pop(domain_num)
                        url_record['visit_at'] = next_visit
                    else:
                        url_record = back_queue.random_pop()
                        url_record['visit_at'] = datetime.now()
                    break
                self.logger.info(f'Fila de URLs vazia. Aguardando...')
                back_cond.wait()
            back_cond.release()

            # Adiciona delay entre downloads do mesmo domínio
            url_record['visit_at'] += timedelta(seconds=self.DELAY_IN_SECONDS)

            # Atualiza o último acesso ao domínio
            self.domain_last_visit[url_record['domain_num']] = url_record['visit_at']

            # Fila de downloads
            download_cond.acquire()
            download_queue.push(url_record)
            download_cond.notify()
            download_cond.release()

            self.logger.debug(f'Download agendado para {url_record["visit_at"]}, '
                              f'URL: {url_trimmer(url_record["url"])}.')
