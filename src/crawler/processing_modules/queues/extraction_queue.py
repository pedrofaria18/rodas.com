from multiprocessing import Queue, Lock, get_logger
from crawler.model.models import DownloadRecord


class ExtractionQueue:
    """
    Fila para extração de links a partir de um documento HTML.
    """

    def __init__(self):
        self.queue = Queue()
        self.__LOCK__ = Lock()
        self.logger = get_logger()
        self.logger.info('Initialized.')

    def get_lock(self) -> Lock:
        return self.__LOCK__

    def push(self, download_record: DownloadRecord) -> None:
        if download_record not in self.queue.queue:
            self.queue.put(download_record)

    def pop(self) -> DownloadRecord | None:
        if self.queue.empty():
            return None
        return self.queue.get()

    def is_empty(self) -> int:
        return self.queue.qsize() == 0
