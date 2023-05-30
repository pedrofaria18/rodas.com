from crawler.processing_modules.domain_extractor import DomainExtractorFactory
from crawler.processing_modules.queues.extraction_queue import ExtractionQueue
from crawler.url_frontier.queues.front_queue import URLFrontQueue
from crawler.logging.log_treatment import url_trimmer
from crawler.model.models import URLRecord
import tldextract

import threading
import logging


class LinkExtractor:
    """
    Esta classe é responsável por extrair os links de uma página HTML, filtrá-los
    e encaminhá-los para a fronteira de URLs.
    """
    def __init__(self, handler: logging.FileHandler):
        self.extractor_factory = DomainExtractorFactory()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info('Iniciado.')

    @staticmethod
    def _remove_insecure_links(url_records: list[URLRecord]) -> list[URLRecord]:
        """Remove links inseguros."""
        filtered_records = []
        for r in url_records:
            if r['url'].startswith('http://'):
                continue
            filtered_records.append(r)
        return filtered_records

    def run(self,
            extraction_cond:   threading.Condition,
            extraction_queue:  ExtractionQueue,
            front_cond:        threading.Condition,
            front_queue:       URLFrontQueue) -> None:
        """Extrai os links do documento HTML e filtra conforme o domínio."""

        self.logger.info(f'Iniciando processo de extração.')

        while True:
            extraction_cond.acquire()
            while True:
                if not extraction_queue.is_empty():
                    download_record = extraction_queue.pop()
                    break
                self.logger.debug(f'Fila de extração vazia. Aguardando...')
                extraction_cond.wait()
            extraction_cond.release()

            url = download_record['url']
            reg_domain = tldextract.extract(url).registered_domain

            extractor = self.extractor_factory.create(registered_domain=reg_domain)
            if not extractor:
                self.logger.error(f'Não existe um módulo de extração para o domínio {reg_domain}.')
                raise NotImplementedError

            # Extrai links da página HTML
            url_recs = extractor.extract(download_record)
            url_recs = extractor.filter(url_recs)
            url_recs = self._remove_insecure_links(url_recs)

            self.logger.info(f'{len(url_recs)} links extraídos da página {url_trimmer(download_record["url"])}.')

            # Encaminha links para a fila do Front
            self.logger.info(f'Encaminhando links para a fila do Front.')

            for r in url_recs:
                front_cond.acquire()
                front_queue.push(r)
                front_cond.notify()
                front_cond.release()

            self.logger.info(f'Encaminhamento concluído.')
