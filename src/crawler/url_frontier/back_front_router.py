from src.crawler.url_frontier.back_queue import URLBackQueue, HostToQueueTable
from src.crawler.url_frontier.front_queue import URLFrontQueue
from urllib.parse import urlparse


class FrontToBackURLRouter:
    """
    Esta classe é responsável por rotear URLs da fila do Front para a fila do Back.
    TODO:
        - Implementar logging para o roteamento de URLs.
    """

    def __init__(self, front_queue: URLFrontQueue, back_queue: URLBackQueue, host_table: HostToQueueTable):
        self.front_queue = front_queue
        self.back_queue = back_queue
        self.host_table = host_table

    def run(self):
        while True:
            if self.front_queue.size() > 0:
                url = self.front_queue.get()
                host_url = urlparse(url).netloc

                queue_num = self.host_table.get_queue_num(host_url)
                self.back_queue.put(url, queue_num)
