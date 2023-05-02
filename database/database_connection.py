from interfaces.i_database_connection import DBConnectionInterface
from database.database_adapters import PersistenceAdapter as adapter
from model.models import DownloadResult, HTMLDocument
import psycopg2


class DBPostgresConnection(DBConnectionInterface):
    """
    Esta classe é responsável por gerenciar a conexão e operações
    com o banco de dados PostgresSQL.
    """

    def __init__(self, user: str, host: str, port: int, db_name: str):
        super().__init__(user, host, port, db_name)
        self.connection = None

    def connect(self, password: str):
        """Conecta ao banco de dados."""
        self.connection = psycopg2.connect(
            user=self.user,
            password=password,
            host=self.host,
            port=self.port,
            database=self.db_name
        )

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.connection.close()

    def insert_html_docs(self, results: list[DownloadResult]) -> bool:
        """Salva os documentos HTML no banco de dados."""
        sql = f"""
        INSERT INTO html_documents (url, url_hash, html, html_hash, updated_at, created_at)
             VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor = self.connection.cursor()
        try:
            values = adapter.parse_to_insert(results)
            cursor.executemany(sql, values)
            self.connection.commit()
        except psycopg2.Error:
            return False
        finally:
            cursor.close()

        return True

    def update_html_docs(self, results: list[DownloadResult]) -> bool:
        """Atualiza o documento HTML no banco de dados."""
        sql = f"""
        UPDATE html_documents as hd
           SET html        = %s,
               html_hash   = %s,
               updated_at  = %s,
               visit_count = hd.visit_count + 1
         WHERE url_hash = %s
        """

        cursor = self.connection.cursor()
        try:
            values = adapter.parse_to_update(results)
            cursor.executemany(sql, values)
            self.connection.commit()
        except psycopg2.Error:
            return False
        finally:
            cursor.close()

        return True

    def delete_html_docs(self, url_hashes: list[str]) -> bool:
        """Deleta o documento HTML no banco de dados."""
        url_hashes = set(url_hashes)
        url_hashes = tuple(url_hashes)

        sql = 'DELETE FROM html_documents WHERE url_hash = %s'

        cursor = self.connection.cursor()
        try:
            cursor.executemany(sql, url_hashes)
            self.connection.commit()
        except psycopg2.Error:
            return False
        finally:
            cursor.close()

        return True

    def get_html_doc_records(self, url_hashes: list[str]) -> dict[any, HTMLDocument] or None:
        """Obtém o documento HTML no banco de dados."""
        url_hashes = set(url_hashes)
        url_hashes = tuple(url_hashes)

        sql = 'SELECT * FROM html_documents WHERE url_hash = %s'

        cursor = self.connection.cursor()
        try:
            cursor.executemany(sql, url_hashes)
            if cursor.rowcount > 0:
                results = cursor.fetchmany(cursor.rowcount)
                records = {adapter.hash(rec): rec for rec in adapter.parse_to_html_docs(results)}
            else:
                records = None
        except psycopg2.Error as e:
            raise Exception(e)
        finally:
            cursor.close()

        return records
