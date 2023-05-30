from crawler.database.db_connector_factory import DBConnectionFactory
from crawler.processing_modules.queues.extraction_queue import ExtractionQueue
from crawler.url_frontier.queues.download_queue import URLDownloadQueue
from crawler.protocol_modules.http_downloader import HTTPDownloader
from crawler.interfaces.i_db_connection import DBConnectionInterface
from crawler.model.models import DownloadRecord, URLRecord, DBConnectionConfig
from datetime import datetime
import asyncio

import threading
import logging


class RewindInputStream:
    """
    Esta classe implementa o módulo de entrada de dados do crawler.

    O módulo de entrada de dados é responsável por:
        - Obter as próximas URLs a serem baixadas;
        - Baixar as páginas HTML;
        - Inserir o conteúdo, os dados e as estatísticas das coletas no banco de dados;
        - Extrair as URLs das páginas HTML;
        - Inserir as URLs extraídas na Fila de Prioridades de URLs;
        - Estabelecer as Políticas de Revisitação das URLs.
    :param handler: Objeto logging.FileHandler
    :param max_wait_time_in_seconds: Tempo máximo de espera por URLs na fila de download.

    TODO:
        - Implementar as políticas de revisitação das URLs.
    """

    def __init__(self, handler: logging.FileHandler, max_wait_time_in_seconds: int = 5):

        self.MAX_WAIT_TIME_IN_SECONDS = max_wait_time_in_seconds
        self.handler = handler

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info(f'Iniciado.')

    def _get_next_urls(self,
                       download_cond: threading.Condition,
                       download_queue: URLDownloadQueue
                       ) -> list[URLRecord] | None:
        """
        Este método é responsável por obter as próximas URLs a serem baixadas. Para garantir o
        menor I/O possível com o banco de dados, é implementado um método de transmissão em rajadas.
        É aguardado até que a fila de download tenha pelo menos uma determinada quantidade de URLs
        ou até que o tempo máximo de espera seja atingido.
        """
        self.logger.info(f'Obtendo novas URLs para download.')

        package = []

        start = datetime.now()
        download_cond.acquire()
        while True:
            if download_queue.is_empty():
                self.logger.debug(f'Fila de download vazia. Aguardando novas URLs...')
                download_cond.wait()
            else:
                record: URLRecord = download_queue.pop()
                package.append(record)
                if download_queue.is_empty():
                    break
        download_cond.release()
        end = datetime.now()

        self.logger.debug(f'Pacote obtido: {len(package)} URLs. '
                          f'Tempo de espera: {(end - start).seconds} segundos.')
        return package

    @staticmethod
    def _aggregate_db_tasks(download_records: list[DownloadRecord],
                            db_connection: DBConnectionInterface
                            ) -> dict[str, list[DownloadRecord]]:

        """Agrupa as tarefas de inserção e atualização do banco de dados."""
        downloaded_recs = [r for r in download_records if 200 <= r['status'] < 300]

        # Checa quais conteúdos já estão no banco de dados
        url_hashes = [r['url_hash'].hexdigest() for r in downloaded_recs]
        db_records = db_connection.select_html_docs(url_hashes)
        if db_records:
            db_html_hashes = set(r['html_hash'] for r in db_records)
            downloaded_recs = [r for r in downloaded_recs if r['html_hash'] not in db_html_hashes]

        return {
            # Apenas conteúdos que não estão no banco serão inseridos, independentemente da url
            'downloaded': downloaded_recs,

            # Falhas serão inseridas em tabela log
            'failed': [r for r in download_records if r['status'] != 200]
        }

    def run(self,
            db_config:        DBConnectionConfig,
            db_pwd:           str,
            download_cond:    threading.Condition,
            download_queue:   URLDownloadQueue,
            extraction_cond:  threading.Condition,
            extraction_queue: ExtractionQueue):
        """
        Executa o módulo de download de páginas.
        :param db_config: Dicionário de configuração de conexão com o banco de dados.
        :param db_pwd: Senha do banco de dados.
        :param download_queue: Fila de URLs a serem baixadas.
        :param extraction_cond: Lock da fila de extração.
        :param extraction_queue: Fila de URLs a serem extraídas.
        :param download_cond: Lock da fila de download.
        """

        self.logger.info(f'Iniciando módulo de entrada de dados.')

        try:
            db_connection = DBConnectionFactory.create(db_config, self.handler)
            db_connection.connect(db_pwd)
        except Exception as e:
            self.logger.error(f'Erro ao conectar ao banco de dados: {e}')
            return

        downloader = HTTPDownloader(self.handler)

        # Loop principal
        while True:
            url_pack = self._get_next_urls(download_cond, download_queue)  # Bloqueante

            self.logger.info(f'Baixando {len(url_pack)} URLs.')

            download_records = asyncio.run(downloader.fetch(url_pack))
            db_tasks = self._aggregate_db_tasks(download_records, db_connection)

            if len(db_tasks['downloaded']) > 0:
                for r in db_tasks['downloaded']:
                    extraction_cond.acquire()
                    extraction_queue.push(r)
                    extraction_cond.notify()
                    extraction_cond.release()
                db_connection.upsert_html_docs(db_tasks['downloaded'])

            if len(db_tasks['failed']) > 0:
                db_connection.upsert_failed_downloads(db_tasks['failed'])

            self.logger.info(f'{len(db_tasks["downloaded"])} documentos baixados, {len(db_tasks["failed"])} falharam.')

