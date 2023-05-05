from crawler.interfaces.i_domain_extractor import DomainExtractorInterface, DomainFilterInterface
from crawler.model.models import Hash, DownloadRecord, URLRecord, URLCategory
from parsel import Selector
import re


class OlxLinkExtractor(DomainExtractorInterface):
    """
    Implementa políticas de seleção de links para o domínio WebMotors.
    Identifica os links que:
        - são anúncios de veículos (leaves) e
        - os links que são páginas de listagem de veículos (seeds).
    """
    @staticmethod
    def search(links: list, rgx: str):
        return [lk for lk in links if re.search(rgx, lk.attrib['href'])]

    def extract(self, download_record: DownloadRecord) -> list[URLRecord]:
        """
        Extrai os links de uma página HTML da OLX
        :param download_record: objeto DownloadRecord
        :return: Lista de links
        """
        html_doc = download_record['html']
        selector = Selector(text=html_doc)

        links = selector.xpath('//a[contains(@href, "olx.com.br/")]')
        categorized_links = {
            URLCategory.LEAF: self.search(links, r'^https://[a-z]{2}.olx.com.br/.+?/autos-e-pecas/'
                                                 r'carros-vans-e-utilitarios/.+$'),
            URLCategory.SEED: self.search(links, r'^https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/.+$')
        }

        url_records = []
        for category, link in categorized_links.items():
            for lk in link:
                url_record: URLRecord = {
                    'url_hash':     Hash(content=lk.attrib['href']),
                    'category':     category,
                    'domain_queue': None,
                    'domain_hash':  Hash('olx.com.br'),
                    'url':          lk.attrib['href']
                }
                url_records.append(url_record)

        return url_records


class OlxLinkFilter(DomainFilterInterface):
    """
    Remove as páginas da WebMotors que não são anúncios de veículos
    TODO: - Implementar a classe
    """
    def filter(self, urls: list[URLRecord]) -> list[URLRecord]:
        """
        Filtra os links de uma página HTML
        :param urls: Lista de objetos URLRecord
        :return: Lista de objetos URLRecord filtrados
        """
        return [r for r in urls if not r['url'].startswith('#')]
