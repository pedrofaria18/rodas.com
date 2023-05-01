from interfaces.ranker import UrlRankerInterface
from multiprocessing import Queue, Lock


class URLFrontQueue:
    """
    Esta classe é responsável por gerenciar as filas do Front de URLs de cada host.
    """

    def __init__(self, ranker: UrlRankerInterface):
        self.url_priority_queues: dict[int, Queue] = dict()
        self.url_count: int = 0
        self.ranker = ranker
        self.lock = Lock()

    def get_lock(self) -> Lock:
        return self.lock

    def put(self, url: str) -> None:
        priority = self.ranker.get_priority(url)
        if priority not in self.url_priority_queues:
            self.url_priority_queues[priority] = Queue()

        self.url_priority_queues[priority].put(url)
        self.url_count += 1

    def get(self) -> str or None:
        if self.url_count == 0:
            return None

        priority = min(self.url_priority_queues.keys())
        url = self.url_priority_queues[priority].get()
        self.url_count -= 1
        return url

    def size(self) -> int:
        return self.url_count


class URLFrontQueueProducer:
    pass
