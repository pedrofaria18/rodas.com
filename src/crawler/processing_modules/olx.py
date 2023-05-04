from crawler.interfaces.i_link_extractor import URLExtractorInterface
from crawler.interfaces.i_url_filter import URLFilterInterface


class OlxURLFilter(URLFilterInterface):
    """
    Remove as páginas da OLX que não são anúncios de veículos

    TODO:
        - Implementar a classe
    """
    def __init__(self):
        pass

    def filter(self, urls: list[str]) -> list[str]:
        return urls


class OlxURLExtractor(URLExtractorInterface):
    """
    Extrai as páginas de anúncios de veículos da OLX a partir de um link seed

    TODO:
        - Implementar a classe.
    """
    def __init__(self):
        pass

    def extract(self, html: str) -> list[str]:
        return []

