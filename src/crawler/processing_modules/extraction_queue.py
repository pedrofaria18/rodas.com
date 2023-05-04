from multiprocessing import Queue, Lock

from crawler.model.models import DownloadRecord


class ExtractionQueue:
    """
    Fila para extração de links a partir de um documento HTML.
    """

    def __init__(self):
        self._queue = Queue()
        self._lock = Lock()

    def push(self, download_record: DownloadRecord) -> None:
        with self._lock:
            self._queue.put(download_record)

    def pop(self) -> DownloadRecord or None:
        with self._lock:
            if self._queue.empty():
                return None
            return self._queue.get()

    def size(self) -> int:
        with self._lock:
            return self._queue.qsize()
