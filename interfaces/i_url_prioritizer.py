from abc import ABC, abstractmethod


class URLPrioritizerInterface(ABC):
    """
    Interface para priorizadores de URLs.
    Um priorizador de URLs recebe uma URL e retorna um valor numérico
    que representa a prioridade de download da URL.
    """
    @abstractmethod
    def get_priority(self, thing) -> int:
        raise NotImplementedError
