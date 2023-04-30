from multiprocessing import Lock

from interfaces.ranker import UrlRankerInterface
from front.queue import FrontQueueHandler
from back.queue import BackQueueHandler


class UrlFrontier:
    front_lock = Lock()
    back_lock = Lock()

    def __init__(self, url_ranker: UrlRankerInterface):
        self.front_queue = FrontQueueHandler(url_ranker)
        self.back_queue = BackQueueHandler()

    def push(self, url: str):
        with self.front_lock:
            self.front_queue.push(url)

    def pop(self) -> str or None:
        self.back_lock.acquire()

        if self.back_queue.size() == 0:
            with self.front_lock:
                self.__refill_back_queue__()

        url = self.back_queue.pop()
        self.back_lock.release()
        return url

    def __refill_back_queue__(self):
        while self.front_queue.size() > 0:
            url = self.front_queue.pop()
            self.back_queue.push(url=url)
