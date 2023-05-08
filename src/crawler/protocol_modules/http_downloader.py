import asyncio

from crawler.model.models import URLRecord, DownloadRecord, Hash
from datetime import datetime
import random
import aiohttp
import threading
import logging


class HTTPDownloader:
    """
    Esta classe é responsável por baixar os conteúdos das páginas
    a partir da Fila de Prioridades de URLS.
    """
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

    def __init__(self, handler: logging.FileHandler):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.logger.info(f'Iniciado.')

    async def __request(self, url_record: URLRecord, responses: list, index: int) -> None:
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
        rand_header = random.sample(self.HEADERS, 1)[0]

        async with aiohttp.ClientSession(headers=rand_header) as session:
            async with session.get(url_record['url']) as response:
                if response.status == 200:
                    result['html'] = await response.text()
                    result['html_hash'] = Hash(content=result['html'])
                result['visited_on'] = datetime.now()
                result['status'] = response.status
                responses[index] = result

    async def fetch(self, urls: list[URLRecord]) -> list[DownloadRecord]:
        """Baixa o conteúdo das URLs informada."""
        logging.info(f'Baixando {len(urls)} páginas.')

        tasks: list[asyncio.Task | None] = [None] * len(urls)
        responses: list[DownloadRecord | None] = [None] * len(urls)

        for i, url in enumerate(urls):
            tasks[i] = asyncio.create_task(self.__request(url, responses, i))

        await asyncio.wait(tasks)

        logging.info(f'Download finalizado.')

        return responses
