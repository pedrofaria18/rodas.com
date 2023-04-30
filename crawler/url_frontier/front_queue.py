from interfaces.ranker import UrlRankerInterface
from multiprocessing import Queue, Lock


class URLFrontQueue:
    """
    Esta classe é responsável por gerenciar as filas do Front de URLs de cada host.
    """

    def __init__(self, ranker: UrlRankerInterface):
        self.url_priority_queues = dict()
        self.url_count = 0
        self.ranker = ranker
        self.lock = Lock()

    def get_lock(self) -> Lock:
        return self.lock

    def put(self, url: str):
        success = False
        try:
            priority = self.ranker.get_priority(url)
            if priority not in self.url_priority_queues:
                self.url_priority_queues[priority] = Queue()

            self.url_priority_queues[priority].put(url)
            self.url_count += 1
            success = True

        except Exception as e:
            print(e)

        finally:
            return success

    def get(self) -> str or None:
        if self.url_count == 0:
            return None

        priority = min(self.url_priority_queues.keys())
        url = self.url_priority_queues[priority].get()
        self.url_count -= 1
        return url

    def get_size(self):
        return self.url_count


class URLFrontQueueProducer:
    pass
