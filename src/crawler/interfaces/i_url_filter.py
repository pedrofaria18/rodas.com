from abc import ABC, abstractmethod


class URLFilterInterface(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def filter(self, urls: list[str]) -> list[str]:
        pass
