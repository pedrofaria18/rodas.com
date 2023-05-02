from src.model.models import DownloadResult, HTMLDocument
from hashlib import md5


class DatabaseParser:
    @staticmethod
    def hash(value: str):
        """Gera um hash MD5 para o valor informado."""
        return md5(value.encode('utf-8'))

    @staticmethod
    def parse_to_html_docs(results: list[tuple]) -> list[HTMLDocument]:
        """Converte os resultados para o formato de salvamento no banco de dados"""
        values = []
        for result in results:
            result_set = HTMLDocument(
                id=result[0],
                url_hash=result[1],
                html_hash=result[2],
                url=result[3],
                html_doc=result[4],
                visit_count=result[5],
                is_active=result[6],
                created_at=result[7],
                visited_at=result[8]
            )
            values.append(result_set)
        return values

    @staticmethod
    def parse_to_insert(results: list[DownloadResult]) -> list[tuple]:
        """Converte os resultados para o formato de salvamento no banco de dados"""
        values = []
        for result in results:
            result_set = (
                result['url'],
                DatabaseParser.hash(result['url']).hexdigest(),
                result['html_doc'],
                DatabaseParser.hash(result['html_doc']).hexdigest()
            )
            values.append(result_set)

        return values

    @staticmethod
    def parse_to_update(results: list[DownloadResult]) -> list[tuple]:
        """Converte os resultados para o formato de salvamento no banco de dados"""
        values = []
        for result in results:
            result_set = (
                result['html_doc'],
                DatabaseParser.hash(result['html_doc']).hexdigest(),
                DatabaseParser.hash(result['url']).hexdigest()
            )
            values.append(result_set)

        return values
