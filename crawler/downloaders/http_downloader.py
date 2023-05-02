from interfaces.i_database_connection import DBConnectionInterface
from database.database_adapters import adapter as adapter
from crawler.downloaders.download_queue import URLDownloadQueue
from model.models import DownloadResult

from datetime import datetime
import aiohttp
import asyncio


class HTTPDownloader:
    """
    Esta classe é responsável por baixar os conteúdos das páginas
    a partir da Fila de Prioridades de URLS.
    """
    MAX_THREADS_NUM = 10
    MAX_CONCURRENT_DOWNLOADS = 20

    def __init__(self, db_connection: DBConnectionInterface, priority_queue: URLDownloadQueue):
        self.db_connection = db_connection
        self.priority_queue = priority_queue
        self.visited_url_hashes = set()

    @staticmethod
    async def __download_url(url: str) -> DownloadResult:
        """Baixa o conteúdo da URL informada."""
        result = DownloadResult(url=url, html_doc=None, status=None, visited_at=None)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    result['html_doc'] = await response.text()
                    result['visited_at'] = datetime.now()
                result['status'] = response.status
                return result

    @staticmethod
    async def download_urls(urls: list[str]) -> list[DownloadResult]:
        """Baixa o conteúdo da URL informada."""
        tasks = [asyncio.create_task(HTTPDownloader.__download_url(url)) for url in urls]
        results = [await task for task in asyncio.as_completed(tasks)]
        return results

    def __get_next_urls(self) -> list or None:
        """Retorna as próximas URLs a serem baixadas."""
        if self.priority_queue.is_empty():
            return None
        urls = []
        while len(urls) <= self.MAX_CONCURRENT_DOWNLOADS:
            if self.priority_queue.is_empty():
                break
            url = self.priority_queue.pop()
            urls.append(url)
        return urls

    def __generate_db_tasks(self, download_results: list):
        """Separa resultados em tarefas de inserção e atualização."""
        tasks = {'insert': [], 'update': [], 'failed': []}

        # Coleta as páginas que falharam e as que não precisam ser checadas contra o banco de dados
        # -----------------------------------------------------------------------------------------
        results_to_check = []
        for result in download_results:
            if result['status'] != 200:
                tasks['failed'].append(result)
                continue

            url_hash = adapter.hash(result['url'])
            if url_hash not in self.visited_url_hashes:
                tasks['insert'].append(result)
                self.visited_url_hashes.add(url_hash)
                continue

            results_to_check.append(result)

        # Checa quais páginas já foram baixadas anteriormente
        # ---------------------------------------------------
        url_hashes = [adapter.hash(result['url']).hexdigest() for result in results_to_check]
        previous_records = self.db_connection.get_html_doc_records(url_hashes)

        # Separa as páginas que precisam ser inseridas e as que precisam ser atualizadas
        # ------------------------------------------------------------------------------
        if previous_records is None:
            map(tasks['insert'].append, results_to_check)
            map(self.visited_url_hashes.add, url_hashes)
            return tasks

        for result in results_to_check:
            url_hash = adapter.hash(result['url'])
            if url_hash not in previous_records:
                tasks['insert'].append(result)
                continue

            if previous_records[url_hash]['html_hash'] != result['html_hash']:
                tasks['update'].append(result)

        return tasks

    async def run(self):
        """Baixa o conteúdo das URLs e salva no banco de dados."""
        while True:
            urls = self.__get_next_urls()
            if urls is None:
                continue

            results = await HTTPDownloader.download_urls(urls)
            db_tasks = self.__generate_db_tasks(results)

            if len(db_tasks['insert_tasks']) > 0:
                self.db_connection.insert_html_docs(db_tasks['insert_tasks'])

            if len(db_tasks['update_tasks']) > 0:
                self.db_connection.update_html_docs(db_tasks['update_tasks'])

            # TODO: Implementar o salvamento de páginas que falharam
            # if len(db_tasks['failed_tasks']) > 0:
            #     self.db_connection.insert_failed_urls(db_tasks['failed_tasks'])
