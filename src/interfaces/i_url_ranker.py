from abc import ABC, abstractmethod


class UrlRankerInterface(ABC):
    @abstractmethod
    def rank_url(self, thing) -> int:
        raise NotImplementedError
