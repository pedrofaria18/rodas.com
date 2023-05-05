from crawler.processing_modules.domain_modules.domain_extractor import DomainExtractorFactory
from crawler.processing_modules.queues.extraction_queue import ExtractionQueue
from crawler.url_frontier.queues.front_queue import URLFrontQueue
from crawler.logging.machinery import url_trimmer
from crawler.model.models import URLRecord
from multiprocessing import get_logger
import tldextract


class LinkExtractor:
    """
    Esta classe é responsável por extrair os links de uma página HTML, filtrá-los
    e encaminhá-los para a fronteira de URLs.
    """
    def __init__(self,
                 extraction_queue:  ExtractionQueue,
                 front_queue:       URLFrontQueue,
                 extractor_factory: DomainExtractorFactory):
        self.extraction_queue = extraction_queue
        self.__EXTRAC_QUEUE_LOCK__ = extraction_queue.get_lock()
        self.front_queue = front_queue
        self.__FRONT_QUEUE_LOCK__ = front_queue.get_lock()
        self.extractor_factory = extractor_factory
        self.logger = get_logger()

    @staticmethod
    def _remove_insecure_links(url_records: list[URLRecord]) -> list[URLRecord]:
        """Remove links inseguros."""
        filtered_records = []
        for r in url_records:
            if r['url'].startswith('http://'):
                continue
            filtered_records.append(r)
        return filtered_records

    def run(self) -> None:
        """Extrai os links do documento HTML e filtra conforme o domínio."""
        while True:
            with self.__EXTRAC_QUEUE_LOCK__:
                if self.extraction_queue.is_empty():
                    continue
                dwnld_record = self.extraction_queue.pop()

            reg_domain = tldextract.extract(dwnld_record['url']).registered_domain

            extractor = self.extractor_factory.create(registered_domain=reg_domain)
            if not extractor:
                self.logger.warning(f'Não existe um módulo de extração para o domínio {reg_domain}.')
                continue

            # Extrai links da página HTML
            url_recs = extractor.extract(dwnld_record)
            url_recs = extractor.filter(url_recs)
            url_recs = self._remove_insecure_links(url_recs)

            self.logger.info(f'{len(url_recs)} links extraídos da página {url_trimmer(dwnld_record["url"])}.')

            # Encaminha links para a fila do Front
            self.logger.info(f'Encaminhando links para a fila do Front.')

            for r in url_recs:
                with self.__FRONT_QUEUE_LOCK__:
                    self.front_queue.push(r)

            self.logger.info(f'Encaminhamento concluído.')
