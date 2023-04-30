from datetime import datetime, timedelta
from time import sleep
import heapq


class BackQueueScheduler:
    def __init__(self):
        self.heap = []
        self.last_visit = dict()

    def append(self, host_key: int, delay_in_sec: int):
        if host_key in self.last_visit:
            start_time = self.last_visit[host_key] + timedelta(seconds=delay_in_sec)
        else:
            start_time = datetime.now()

        heapq.heappush(self.heap, (start_time, host_key))

    def get_next_host(self) -> int or None:
        if len(self.heap) == 0:
            return None

        start_time, host_key = heapq.heappop(self.heap)

        while start_time > datetime.now():
            sleep(1)

        self.last_visit[host_key] = datetime.now()

        return host_key
