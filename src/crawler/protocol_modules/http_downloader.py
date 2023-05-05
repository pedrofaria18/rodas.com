from crawler.model.models import URLRecord, DownloadRecord, Hash
from multiprocessing import get_logger
from datetime import datetime
import random
import aiohttp
import asyncio

HEADERS = [
    # Samsung Galaxy S22
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, '
                   'like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36'},
    # Samsung Galaxy S21
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, '
                   'like Gecko) Version/4.0 Mobile Safari/537.36'},
    # Samsung Galaxy S20
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G980F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, '
                   'like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36'},
]


class HTTPDownloader:
    """
    Esta classe é responsável por baixar os conteúdos das páginas
    a partir da Fila de Prioridades de URLS.
    """
    def __init__(self):
        self.logger = get_logger()
        self.logger.info('Inicializado.')
        self.headers = HEADERS

    async def __request(self, url_record: URLRecord) -> DownloadRecord:
        """Baixa o conteúdo da URL informada."""
        result: DownloadRecord = {
            'url_hash':   Hash(content=url_record['url']),
            'html_hash':  None,
            'category':   url_record['category'],
            'url':        url_record['url'],
            'html':       None,
            'status':     None,
            'visited_on': None
        }
        # Seleciona um User-Agent aleatório.
        rand_header = random.sample(self.headers, 1)[0]

        async with aiohttp.ClientSession(headers=rand_header) as session:
            async with session.get(url_record['url']) as response:
                if response.status == 200:
                    result['html'] = await response.text()
                    result['html_hash'] = Hash(content=result['html'])
                result['visited_on'] = datetime.now()
                result['status'] = response.status
                return result

    async def fetch(self, urls: list[URLRecord]) -> list[DownloadRecord]:
        """Baixa o conteúdo das URLs informada."""
        self.logger.info(f'Baixando {len(urls)} páginas.')

        tasks = [asyncio.create_task(self.__request(url)) for url in urls]
        responses = [await task for task in asyncio.as_completed(tasks)]

        self.logger.info('Download finalizado.')

        return responses
