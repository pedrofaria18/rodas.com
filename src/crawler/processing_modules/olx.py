from src.interfaces.i_link_extractor import LinkExtractorInterface
from src.interfaces.i_url_filter import URLFilterInterface


class OlxURLFilter(URLFilterInterface):
    """
    Remove as páginas da OLX que não são anúncios de veículos

    TODO:
        - Implementar a classe
    """
    pass


class OlxLinkExtractor(LinkExtractorInterface):
    """
    Extrai as páginas de anúncios de veículos da OLX a partir de um link seed

    TODO:
        - Implementar a classe.
    """
    pass
