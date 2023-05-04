from crawler.model.models import DownloadRecord, Hash
from datetime import datetime
import aiohttp
import asyncio


class HTTPDownloader:
    """
    Esta classe é responsável por baixar os conteúdos das páginas
    a partir da Fila de Prioridades de URLS.
    """
    @staticmethod
    async def __request(url: str) -> DownloadRecord:
        """Baixa o conteúdo da URL informada."""
        result = DownloadRecord(
            url=url,
            url_hash=Hash(url),
            html_hash=None,
            html=None,
            status=None,
            visited_on=None
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    result['html'] = await response.text()
                    result['html_hash'] = Hash(result['html'])
                result['visited_on'] = datetime.now()
                result['status'] = response.status
                return result

    @staticmethod
    async def fetch(urls: list[str]) -> list[DownloadRecord]:
        """Baixa o conteúdo das URLs informada."""
        tasks = [asyncio.create_task(HTTPDownloader.__request(url)) for url in urls]
        responses = [await task for task in asyncio.as_completed(tasks)]
        return responses
