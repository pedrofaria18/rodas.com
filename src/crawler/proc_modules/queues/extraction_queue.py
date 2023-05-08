import logging
from collections import deque
from crawler.model.models import DownloadRecord


class ExtractionQueue:
    """
    Fila para extração de links a partir de um documento HTML.
    """

    def __init__(self, handler: logging.FileHandler):
        self.queue = deque()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info('Iniciada.')

    def push(self, download_record: DownloadRecord) -> None:
        self.queue.append(download_record)

    def pop(self) -> DownloadRecord:
        return self.queue.popleft()

    def is_empty(self) -> int:
        return len(self.queue) == 0
