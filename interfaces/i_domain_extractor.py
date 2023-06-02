from abc import ABC, abstractmethod

from crawler.model.models import DownloadRecord, URLRecord


class DomainExtractorInterface(ABC):
    """
    Interface para extração de links
    """

    @abstractmethod
    def extract(self, download_record: DownloadRecord) -> list[URLRecord]:
        pass


class DomainFilterInterface(ABC):
    """
    Interface para filtragem de links
    """

    @abstractmethod
    def filter(self, urls: list[URLRecord]) -> list[URLRecord]:
        pass
