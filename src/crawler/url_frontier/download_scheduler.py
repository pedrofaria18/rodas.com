from crawler.url_frontier.queues.download_queue import URLDownloadQueue
from crawler.url_frontier.queues.back_queue import URLBackQueue
from crawler.logging.machinery import url_trimmer
from multiprocessing import get_logger
from datetime import datetime, timedelta


class URLDownloadScheduler:
    """
    Esta classe é responsável por agendar o download de URLs.
    TODO:
        - Avaliar se vale a pena implementar leitura de `robots.txt` para delays.
        - Implementar salvamento de estado no banco de dados em caso de falha crítica.
    """

    DELAY_IN_SECONDS = 10

    def __init__(self,
                 back_queue: URLBackQueue,
                 download_queue: URLDownloadQueue,
                 delay_in_seconds: int = 10):

        self.back_queue = back_queue
        self.__BACK_QUEUE_LOCK__ = back_queue.get_lock()

        self.download_queue = download_queue
        self.__DWNLD_QUEUE_LOCK__ = download_queue.get_lock()

        self.DELAY_IN_SECONDS = delay_in_seconds

        self.domain_last_visit = dict()

        self.logger = get_logger()
        self.logger.info('Inicializado.')

    def _set_domain_last_visit(self, domain_queue: int, last_visit: datetime) -> None:
        """ Define a última visita ao host. """
        self.domain_last_visit[domain_queue] = last_visit

    def _get_domain_next_visit(self) -> (int | None, datetime | None):
        """ Retorna o próximo host a ser visitado. """
        if not self.domain_last_visit:
            self.logger.warning('Ainda não há domínios visitados!')
            return None, None

        min_datetime = min(self.domain_last_visit.values())
        domain_num = next((d for d, lv in self.domain_last_visit.items() if lv == min_datetime), None)
        if domain_num is None:
            return None, None

        next_visit = min_datetime + timedelta(seconds=self.DELAY_IN_SECONDS)
        self._set_domain_last_visit(domain_num, next_visit)

        return domain_num, next_visit

    def run(self):
        """ Executa o agendamento de downloads. """
        while True:
            with self.__BACK_QUEUE_LOCK__:
                if self.back_queue.is_empty():
                    continue
                domain_num, next_visit = self._get_domain_next_visit()
                if not domain_num:
                    url_record = self.back_queue.random_pop()
                    next_visit = datetime.now() + timedelta(seconds=self.DELAY_IN_SECONDS)
                else:
                    url_record = self.back_queue.pop(domain_num)

            with self.__DWNLD_QUEUE_LOCK__:
                self._set_domain_last_visit(url_record['domain_queue'], next_visit)
                self.download_queue.push(url_record, next_visit)

            self.logger.info(f'Download agendado para {next_visit}, URL: {url_trimmer(url_record["url"])}.')
