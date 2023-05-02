from src.interfaces.i_link_extractor import LinkExtractorInterface
from src.interfaces.i_url_filter import URLFilterInterface


class WebMotorsURLFilter(URLFilterInterface):
    """
    Remove as páginas da WebMotors que não são anúncios de veículos

    TODO:
        - Implementar a classe
    """
    pass


class WebMotorsLinkExtractor(LinkExtractorInterface):
    """
    Extraí as páginas de anúncios de veículos da WebMotors a partir de um link seed

    TODO:
        - Implementar a classe.
    """
    pass
