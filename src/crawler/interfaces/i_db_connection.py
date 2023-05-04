from crawler.model.models import DownloadRecord
from abc import ABC, abstractmethod


class DBConnectionInterface(ABC):
    """
    Esta classe é responsável por gerenciar a conexão com o banco de dados.
    """
    @abstractmethod
    def __init__(self, user: str, host: str, port: int, db_name: str):
        self.user = user
        self.host = host
        self.port = port
        self.db_name = db_name

    @abstractmethod
    def connect(self, password: str):
        """Conecta ao banco de dados."""
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """Fecha a conexão com o banco de dados."""
        raise NotImplementedError

    @staticmethod
    def parse_results(results: list[DownloadRecord]) -> list[set]:
        """Converte os resultados para o formato de salvamento no banco de dados"""
        raise NotImplementedError

    @abstractmethod
    def insert_html_docs(self, results: list[DownloadRecord]):
        """Salva o documento HTML no banco de dados."""
        raise NotImplementedError

    @abstractmethod
    def delete_html_docs(self, url_hashes: list[str]):
        """Deleta o documento HTML no banco de dados."""
        raise NotImplementedError

    @abstractmethod
    def select_html_docs(self, url_hashes: list[str]) -> dict[any, DownloadRecord] or None:
        """Retorna o documento HTML no banco de dados."""
        raise NotImplementedError

    @abstractmethod
    def insert_failed_downloads(self, results: list[DownloadRecord]) -> bool:
        """Salva os downloads falhos no banco de dados."""
        raise NotImplementedError
