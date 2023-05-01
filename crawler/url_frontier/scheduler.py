from crawler.url_frontier.back_queue import URLBackQueue, HostToQueueTable
from crawler.url_frontier.priority_queue import URLDownloadQueue


class URLDownloadScheduler:
    """
    Esta classe é responsável por agendar o download de URLs.
    """
    def __init__(self, back_queue: URLBackQueue, download_queue: URLDownloadQueue, host_table: HostToQueueTable):
        self.host_table = host_table
        self.back_queue = back_queue
        self.download_queue = download_queue
        self.host_last_visit = dict()

    def get_host_last_visit(self, host_num: int) -> datetime:
        if host_num not in self.host_last_visit:
            self.host_last_visit[host_num] = datetime.now()

        return self.host_last_visit[host_num]

    def set_host_last_visit(self, host_num: int, last_visit: datetime) -> None:
        self.host_last_visit[host_num] = last_visit

    # def run(self):
    #     while True:
    #