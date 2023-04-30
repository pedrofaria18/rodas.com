from collections import deque
from urllib.parse import urlparse
from multiprocessing import Lock

from router import BackQueueRouter
from scheduler import BackQueueScheduler


class BackQueueHandler:
    # Delay em segundos entre cada visita a um mesmo domínio (host)
    DELAY_IN_SEC = 10

    def __init__(self):
        self.router = BackQueueRouter()
        self.scheduler = BackQueueScheduler()
        self.url_queues = dict()
        self.url_count = 0

    def size(self):
        return self.url_count

    def push(self, url: str):
        host_url = urlparse(url).netloc
        host_key = self.router.get_host_key(host_url=host_url)

        if host_key not in self.url_queues:
            self.url_queues[host_key] = deque()

        self.scheduler.append(host_key=host_key, delay_in_sec=self.DELAY_IN_SEC)
        self.url_queues[host_key].push(url)
        self.url_count += 1

    def pop(self) -> str or None:
        if self.url_count == 0:
            return None

        host_key = self.scheduler.get_next_host()
        if host_key is None:
            return None

        url = self.url_queues[host_key].popleft()
        self.url_count -= 1
        return url
