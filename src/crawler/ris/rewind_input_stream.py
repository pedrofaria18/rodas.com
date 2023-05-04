from crawler.processing_modules.extraction_queue import ExtractionQueue
from crawler.protocol_modules.http_downloader import HTTPDownloader
from crawler.url_frontier.download_queue import URLDownloadQueue
from crawler.interfaces.i_db_connection import DBConnectionInterface
from crawler.model.models import DownloadRecord


class RewindInputStream:

    _MAX_TASK_PACKAGE_SIZE = 100

    def __init__(self,
                 connection: DBConnectionInterface,
                 download_queue: URLDownloadQueue,
                 extraction_queue: ExtractionQueue):
        self.db_connection = connection
        self.download_queue = download_queue
        self.extraction_queue = extraction_queue
        self.downloader = HTTPDownloader()

    def _get_next_urls(self) -> list[str] or None:
        """Retorna as próximas URLs a serem baixadas."""
        if self.download_queue.is_empty():
            return None
        urls = []
        while len(urls) <= self._MAX_TASK_PACKAGE_SIZE and not self.download_queue.is_empty():
            url = self.download_queue.pop()
            urls.append(url)
        return urls

    def _aggregate_db_tasks(self, download_records: list[DownloadRecord]):
        """Agrupa as tarefas de inserção e atualização no banco de dados."""
        downloaded_recs = [r for r in download_records if 200 <= r['status'] < 300]
        url_hashes = [r['url_hash'].hexdigest() for r in downloaded_recs]

        # Checa quais conteúdos já estão no banco de dados
        db_records = self.db_connection.select_html_docs(url_hashes)
        db_html_hashes = set(rec['html_hash'] for rec in db_records)

        tasks = {
            # Apenas conteúdos que não estão no banco serão inseridos, independentemente da url
            'insert': [d for d in downloaded_recs if d['html_hash'] not in db_html_hashes],

            # Falhas serão inseridas em tabela log
            'failed': [r for r in download_records if r['status'] != 200]
        }
        return tasks

    async def run(self):
        """Executa o módulo de download de páginas."""
        while True:
            urls = self._get_next_urls()
            if urls is None:
                continue

            download_records = await self.downloader.fetch(urls)
            database_tasks = self._aggregate_db_tasks(download_records)

            if len(database_tasks['insert']) > 0:
                self.db_connection.insert_html_docs(database_tasks['insert'])
                # Insere documentos HTML na fila para extração
                map(self.extraction_queue.push, database_tasks['insert'])

            if len(database_tasks['failed']) > 0:
                self.db_connection.insert_failed_downloads(database_tasks['failed'])
