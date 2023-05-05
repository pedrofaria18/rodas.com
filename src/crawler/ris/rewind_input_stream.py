from crawler.processing_modules.queues.extraction_queue import ExtractionQueue
from crawler.url_frontier.queues.download_queue import URLDownloadQueue
from crawler.protocol_modules.http_downloader import HTTPDownloader
from crawler.interfaces.i_db_connection import DBConnectionInterface
from crawler.model.models import DownloadRecord, URLRecord
from multiprocessing import get_logger
from datetime import datetime


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

    :param connection: Conexão com o banco de dados.
    :param download_queue: Fila de URLs a serem baixadas.
    :param extraction_queue: Fila de URLs a serem extraídas.
    :param max_downloads_per_cycle: Número máximo de downloads por ciclo.
    :param max_wait_time_in_seconds: Tempo máximo de espera por URLs na fila de download.

    TODO:
        - Implementar as políticas de revisitação das URLs.
    """

    def __init__(self,
                 connection:               DBConnectionInterface,
                 download_queue:           URLDownloadQueue,
                 extraction_queue:         ExtractionQueue,
                 max_downloads_per_cycle:  int = 500,
                 max_wait_time_in_seconds: int = 5):

        self.download_queue = download_queue
        self.__DWNLD_QUEUE_LOCK__ = download_queue.get_lock()

        self.extraction_queue = extraction_queue
        self.__EXTRAC_QUEUE_LOCK__ = extraction_queue.get_lock()

        self.downloader = HTTPDownloader()
        self.db_connection = connection

        self.MAX_DOWNLOADS_PER_CYCLE = max_downloads_per_cycle
        self.MAX_WAIT_TIME_IN_SECONDS = max_wait_time_in_seconds

        self.logger = get_logger()
        self.logger.info('Inicializado.')

    def _get_next_urls(self) -> list[URLRecord] | None:
        """
        Este método é responsável por obter as próximas URLs a serem baixadas. Para garantir o
        menor I/O possível com o banco de dados, é implementado um método de transmissão em rajadas.
        É aguardado até que a fila de download tenha pelo menos uma determinada quantidade de URLs
        ou até que o tempo máximo de espera seja atingido.
        """
        package = []

        start = datetime.now()
        while (datetime.now() - start).seconds <= self.MAX_WAIT_TIME_IN_SECONDS or\
                len(package) <= self.MAX_DOWNLOADS_PER_CYCLE:

            with self.__DWNLD_QUEUE_LOCK__:
                if self.download_queue.is_empty():
                    continue
                record: URLRecord = self.download_queue.pop()
                package.append(record)
        end = datetime.now()

        if len(package) == 0:
            url_package = None
            log_msg = 'Nenhuma URL obtida.'
        else:
            url_package = package
            log_msg = f'Pacote obtido: {len(package)} URLs.'

        self.logger.debug(f'{log_msg} Tempo de espera: {(end - start).seconds} segundos.')

        return url_package

    def _aggregate_db_tasks(self, download_records: list[DownloadRecord]):
        """Agrupa as tarefas de inserção e atualização do banco de dados."""
        downloaded_recs = [r for r in download_records if 200 <= r['status'] < 300]
        url_hashes = [r['url_hash'].hexdigest() for r in downloaded_recs]

        # Checa quais conteúdos já estão no banco de dados
        db_records = self.db_connection.select_html_docs(url_hashes)
        db_html_hashes = set(r['html_hash'] for r in db_records)

        return {
            # Apenas conteúdos que não estão no banco serão inseridos, independentemente da url
            'downloaded': [r for r in downloaded_recs if r['html_hash'] not in db_html_hashes],

            # Falhas serão inseridas em tabela log
            'failed': [r for r in download_records if r['status'] != 200]
        }

    async def run(self):
        """Executa o módulo de download de páginas."""
        while True:
            urls = self._get_next_urls()          # Este método é bloqueante da fila de download
            if urls is None:
                continue

            download_records = await self.downloader.fetch(urls)
            db_tasks = self._aggregate_db_tasks(download_records)

            self.logger.info(f'{len(db_tasks["insert"])} documentos baixados, '
                             f'{len(db_tasks["failed"])} falharam.')

            if len(db_tasks['downloaded']) > 0:
                # Insere documentos HTML no banco de dados
                self.db_connection.upsert_html_docs(db_tasks['downloaded'])
                # Insere documentos HTML na fila de extração
                for r in db_tasks['downloaded']:
                    with self.__EXTRAC_QUEUE_LOCK__:
                        self.extraction_queue.push(r)

            if len(db_tasks['failed']) > 0:
                # Insere log de falhas no banco de dados
                self.db_connection.upsert_failed_downloads(db_tasks['failed'])
