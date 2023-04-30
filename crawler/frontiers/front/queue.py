from interfaces.ranker import UrlRankerInterface
from collections import deque


class FrontQueueHandler:
    def __init__(self, url_ranker: UrlRankerInterface):
        self.ranker = url_ranker
        self.url_queues = dict()
        self.url_count = 0

    def size(self):
        return self.url_count

    def push(self, url):
        priority = self.ranker.get_priority(url)

        if priority not in self.url_queues:
            self.url_queues[priority] = deque()

        self.url_queues[priority].push(url)
        self.url_count += 1

    def pop(self):
        if self.url_count == 0:
            return None

        priority = min(self.url_queues.keys())
        url = self.url_queues[priority].popleft()
        self.url_count -= 1
        return url
