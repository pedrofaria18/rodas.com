from crawler.proc_modules.domain_modules.webmotors import WebMotorsLinkExtractor, WebMotorsLinkFilter
from crawler.proc_modules.domain_modules.olx import OlxLinkExtractor, OlxLinkFilter
from crawler.interfaces.i_domain_extractor import DomainExtractorInterface, DomainFilterInterface
from crawler.model.models import DownloadRecord, URLRecord
import logging


class DomainExtractor(DomainExtractorInterface, DomainFilterInterface):
    """
    Esta classe é responsável por extrair os links de uma página HTML e filtrá-los
    segundo o domínio.
    :param extractor: Instância de um objeto que implementa a interface DomainExtractorInterface.
    :param _filter: Instância de um objeto que implementa a interface DomainFilterInterface.
    """
    def __init__(self, extractor: DomainExtractorInterface, _filter: DomainFilterInterface):
        self._extractor = extractor
        self._filter = _filter

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info('Iniciado.')

    def extract(self, download_record: DownloadRecord) -> list[URLRecord]:
        """Extrai os links da página HTML conforme o domínio."""
        try:
            return self._extractor.extract(download_record)
        except Exception as e:
            self.logger.error(f'Erro ao extrair links: {e}')
            raise e

    def filter(self, url_records: list[URLRecord]) -> list[URLRecord]:
        """Filtra os links conforme o domínio"""
        try:
            return self._filter.filter(url_records)
        except Exception as e:
            self.logger.error(f'Erro ao filtrar links: {e}')
            raise e


class DomainExtractorFactory:
    """
    Esta classe cria instâncias de LinkExtractor para cada domínio.
    """
    __DOMAIN_MODULES__ = {
        hash('olx.com.br'): {'extractor': OlxLinkExtractor(), 'filter': OlxLinkFilter()},
        hash('webmotors.com.br'): {'extractor': WebMotorsLinkExtractor(), 'filter': WebMotorsLinkFilter()}
    }

    def create(self, registered_domain: str) -> DomainExtractor | None:
        """Cria um DomainExtractor para o domínio especificado."""
        domain_key = hash(registered_domain)
        if domain_key not in self.__DOMAIN_MODULES__:
            return None

        module = self.__DOMAIN_MODULES__[domain_key]
        return DomainExtractor(extractor=module['extractor'], _filter=module['filter'])
