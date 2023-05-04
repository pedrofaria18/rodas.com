from crawler.processing_modules.extraction_queue import ExtractionQueue
from crawler.url_frontier.front_queue import URLFrontQueue
from crawler.interfaces.i_link_extractor import URLExtractorInterface
from crawler.interfaces.i_url_filter import URLFilterInterface
from multiprocessing import Queue, Lock, get_logger


class LinkExtractor:
    """
    Esta classe é responsável por extrair os links de uma página HTML, filtrá-los
    e encaminhá-los para a fronteira de URLs.
    """
    def __init__(self,
                 extractor: URLExtractorInterface,
                 url_filter: URLFilterInterface,
                 extraction_queue: ExtractionQueue,
                 front_queue: URLFrontQueue):
        self.extraction_queue = extraction_queue
        self.front_queue = front_queue
        self.link_extractor = extractor
        self.url_filter = url_filter
        self.logger = get_logger()

    def run(self) -> None:
        """Extrai os links da página HTML e os filtra"""
        while True:
            if self.extraction_queue.size() > 0:
                # Coleta URL da fila de extração
                download_record = self.extraction_queue.pop()
                url = download_record.url
                html = download_record.html

                # Extrai links da página HTML
                links = self.link_extractor.extract_links(url, html)

                # Filtra links
                links = self.url_filter.filter_links(url, links)

                # Encaminha links para a fila do Front
                for link in links:
                    self.front_queue.push(link)

                self.logger.info(f"LinkExtractor: {len(links)} links extracted from {url}")