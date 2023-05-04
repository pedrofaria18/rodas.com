from crawler.processing_modules.webmotors import WebMotorsURLExtractor, WebMotorsURLFilter
from crawler.processing_modules.olx import OlxURLExtractor, OlxURLFilter
from crawler.processing_modules.link_extractor import LinkExtractor


class LinkExtractorFactory:
    """
    Esta classe cria instâncias de LinkExtractor para cada domínio.
    """

    def __init__(self):
        self._modules = {
            hash('www.olx.com.br'): {'extractor': OlxURLExtractor(), 'filter': OlxURLFilter()},
            hash('www.webmotors.com.br'): {'extractor': WebMotorsURLExtractor(), 'filter': WebMotorsURLFilter()}
        }

    def create(self, domain: str) -> LinkExtractor:
        """Cria um LinkExtractor para o domínio especificado."""
        if hash(domain) not in self._modules:
            raise ValueError(f'Não existe um módulo de extração para o domínio {domain}.')

        domain_modules = self._modules[hash(domain)]
        return LinkExtractor(extractor=domain_modules['extractor'], url_filter=domain_modules['filter'])
