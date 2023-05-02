from abc import ABC, abstractmethod


class UrlRankerInterface(ABC):
    @abstractmethod
    def get_priority(self, thing) -> int:
        raise NotImplementedError
