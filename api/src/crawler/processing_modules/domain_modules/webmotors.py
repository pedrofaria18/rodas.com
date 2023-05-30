from crawler.interfaces.i_domain_extractor import DomainExtractorInterface, DomainFilterInterface
from crawler.model.models import DownloadRecord, URLRecord

DOMAIN_URL = 'www.webmotors.com.br'


class WebMotorsLinkExtractor(DomainExtractorInterface):
    """
    Implementa políticas de seleção de links para o domínio WebMotors
    """
    def extract(self, download_record: DownloadRecord) -> list[URLRecord]:
        """
        Extrai os links de uma página HTML
        :param download_record: Documento HTML
        :return: Lista de links
        """
        raise NotImplementedError


class WebMotorsLinkFilter(DomainFilterInterface):
    """
    Remove as páginas da WebMotors que não são anúncios de veículos
    TODO: - Implementar a classe
    """
    def filter(self, urls: list[URLRecord]) -> list[URLRecord]:
        """
        Filtra os links de uma página HTML
        :param urls: Lista de links
        :return: Lista de links filtrados
        """
        raise NotImplementedError
