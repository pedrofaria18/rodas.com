from urllib.parse import urlparse
from datetime import datetime
from crawler.url_frontier.front_queue import URLFrontQueue
from crawler.url_frontier.priority_queue import URLDownloadQueue
from multiprocessing import Queue, Lock


class URLBackQueue:
    """
    Esta classe é responsável por gerenciar as filas de URLs de cada host.
    """

    def __init__(self):
        self.url_host_queues = dict()
        self.url_count = 0
        self.lock = Lock()

    def get_lock(self) -> Lock:
        return self.lock

    def put(self, url: str, queue_num: int):
        with self.lock:
            if queue_num not in self.url_host_queues:
                self.url_host_queues[queue_num] = Queue()

            self.url_host_queues[queue_num].put(url)
            self.url_count += 1

    def get(self, host_num: int) -> str or None:
        with self.lock:
            if self.url_count == 0:
                return None

            if host_num not in self.url_host_queues:
                return None

            url = self.url_host_queues[host_num].get()
            self.url_count -= 1
            return url

    def size(self):
        return self.url_count


class HostToQueueTable:
    """
    Esta classe é responsável por mapear cada host/domínio para uma fila de URLs.
    """

    def __init__(self):
        self.host_to_queue_table = dict()
        self.lock = Lock()

    def get_queue_num(self, host_url) -> int:
        with self.lock:
            host_key = hash(host_url)
            if host_key not in self.host_to_queue_table:
                self.host_to_queue_table[host_key] = len(self.host_to_queue_table)

            return self.host_to_queue_table[host_key]


class URLFrontToBackRouter:
    """
    Esta classe é responsável por rotear URLs da fila do Front para a fila do Back.
    """

    def __init__(self, front_queue: URLFrontQueue, back_queue: URLBackQueue, host_table: HostToQueueTable):
        self.front_queue = front_queue
        self.back_queue = back_queue
        self.host_table = host_table

    def run(self):
        while True:
            if self.front_queue.get_size() > 0:
                url = self.front_queue.get()
                host_url = urlparse(url).netloc

                queue_num = self.host_table.get_queue_num(host_url)
                self.back_queue.put(url, queue_num)


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

    def run(self):
        while True:
            url = self.back_queue.get()
            if url is None:
                break

            self.download_queue.push(url)
