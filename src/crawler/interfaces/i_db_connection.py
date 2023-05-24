import logging

from crawler.model.models import DownloadRecord, DBConnectionConfig, DatabaseDocForProcess
from abc import ABC, abstractmethod


class DBConnectionInterface(ABC):
    """
    Esta classe é responsável por gerenciar a conexão com o banco de dados.
    """
    @abstractmethod
    def __init__(self, db_config: DBConnectionConfig, handler: logging.FileHandler):
        self.db_config = db_config

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

    @abstractmethod
    def select_docs_for_processing(self, is_active: bool) -> list[DatabaseDocForProcess] | None:
        """Obtém os registros para o processamento dos documentos e inserção no elastic."""
        raise NotImplementedError

    @abstractmethod
    def update_processing_date(self, records: list[DatabaseDocForProcess]) -> bool:
        """Atualiza a data de processamento dos registros."""
        raise NotImplementedError
