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

    @abstractmethod
    def select_html_docs(self, url_hashes: list[str]) -> dict[any, DownloadRecord] | None:
        """Obtém os registros de documentos HTML salvos no banco de dados."""
        raise NotImplementedError

    @abstractmethod
    def upsert_html_docs(self, results: list[DownloadRecord]) -> bool:
        """Salva ou atualiza os registros de documentos HTML no banco de dados."""
        raise NotImplementedError

    @abstractmethod
    def delete_html_docs(self, url_hashes: list[str]) -> bool:
        """Deleta o documento HTML no banco de dados."""
        raise NotImplementedError

    @abstractmethod
    def upsert_failed_downloads(self, results: list[DownloadRecord]) -> bool:
        """Salva ou atualiza os registros de downloads falhos no banco de dados."""
        raise NotImplementedError
