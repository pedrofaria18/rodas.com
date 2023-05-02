from src.crawler.url_frontier.download_queue import URLDownloadQueue
from src.crawler.url_frontier.back_queue import URLBackQueue, HostToQueueTable
from datetime import datetime, timedelta


class URLDownloadScheduler:
    """
    Esta classe é responsável por agendar o download de URLs.
    """

    # TODO:
    #  - Implementar logging para o scheduler.
    #  - Avaliar se vale a pena implementar leitura de `robots.txt` para delays.

    DELAY_IN_SECONDS = 5

    def __init__(self, back_queue: URLBackQueue, download_queue: URLDownloadQueue, host_table: HostToQueueTable):
        self.host_table = host_table
        self.back_queue = back_queue
        self.download_queue = download_queue
        self.host_last_visit = dict()

    def _set_host_last_visit(self, host_num: int, last_visit: datetime) -> None:
        """ Define a última visita ao host. """
        self.host_last_visit[host_num] = last_visit

    def _get_next_host_visit(self) -> (int or None, datetime or None):
        """ Retorna o próximo host a ser visitado. """
        if len(self.host_last_visit) == 0:
            return None, None

        min_datetime = min(self.host_last_visit.values())
        for host, last_visit in self.host_last_visit.items():
            if last_visit == min_datetime:
                next_visit = min_datetime + timedelta(seconds=self.DELAY_IN_SECONDS)
                self._set_host_last_visit(host, next_visit)
                return host, next_visit

    def run(self):
        while True:
            host_num, next_visit = self._get_next_host_visit()
            if host_num is None:
                continue

            if next_visit > datetime.now():
                continue

            url = self.back_queue.get(host_num)
            if url is None:
                continue

            self.download_queue.push(url, next_visit)
