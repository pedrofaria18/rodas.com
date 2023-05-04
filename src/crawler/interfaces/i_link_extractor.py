from abc import ABC, abstractmethod


class URLExtractorInterface(ABC):
    """Interface para extração de links"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def extract(self, html: str) -> list:
        pass
