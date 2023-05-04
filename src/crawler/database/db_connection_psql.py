from crawler.interfaces.i_db_connection import DBConnectionInterface
from crawler.model.models import DownloadRecord, HTMLDocumentRecord, Hash
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

    def insert_html_docs(self, download_records: list[DownloadRecord]) -> bool:
        """Salva os documentos HTML no banco de dados."""
        cursor = self.connection.cursor()
        try:
            sql = '''
            INSERT INTO html_document (url_hash, html_hash, url, html, last_visit_on, first_visit_on)
            VALUES (%(url_hash)s, %(html_hash)s, %(url)s, %(html)s, %(visited_on)s, %(visited_on)s)
            ON CONFLICT (url_hash) DO UPDATE
                SET html_hash     = EXCLUDED.html_hash,
                    html          = EXCLUDED.html,
                    last_visit_on = EXCLUDED.last_visit_on
            '''
            values = [{
                'url_hash':   dr['url_hash'].hexdigest(),
                'html_hash':  dr['html_hash'].hexdigest(),
                'url':        dr['url'],
                'html':       dr['html'],
                'visited_on': dr['visited_on']
            } for dr in download_records]

            cursor.executemany(sql, values)
            self.connection.commit()

        except psycopg2.Error:
            return False
        finally:
            cursor.close()
        return True

    def delete_html_docs(self, url_hashes: list[str]) -> bool:
        """Deleta o documento HTML no banco de dados."""
        cursor = self.connection.cursor()
        try:
            sql = 'DELETE FROM html_document WHERE url_hash = %s'
            cursor.executemany(sql, tuple(set(url_hashes)))
            self.connection.commit()
        except psycopg2.Error:
            return False
        finally:
            cursor.close()
        return True

    def select_html_docs(self, url_hashes: list[str]) -> list[HTMLDocumentRecord] or None:
        """Obtém o documento HTML no banco de dados."""
        cursor = self.connection.cursor()
        try:
            sql = '''
            SELECT id,
                   url_hash,
                   html_hash,
                   num_of_downloads,
                   last_visit_on,
                   first_visit_on
              FROM html_document
             WHERE url_hash = %s
            '''

            cursor.executemany(sql, tuple(set(url_hashes)))
            if cursor.rowcount == 0:
                records = None
            else:
                records = cursor.fetchmany(cursor.rowcount)
                records = [
                    HTMLDocumentRecord(
                      id=rec[0],
                      url_hash=Hash(hex_hash=rec[1]),
                      html_hash=Hash(hex_hash=rec[2]),
                      num_of_downloads=rec[3],
                      last_visit_on=rec[4],
                      first_visit_on=rec[5]
                    ) for rec in records
                ]
        except psycopg2.Error as e:
            raise Exception(e)
        finally:
            cursor.close()

        return records

    def insert_failed_downloads(self, download_records: list[DownloadRecord]) -> bool:
        """Salva os downloads falhos no banco de dados."""
        cursor = self.connection.cursor()
        try:
            sql = '''
            INSERT INTO failed_download_log (url_hash, url, last_status, last_fail_on, first_fail_on)
            VALUES (%(url_hash)s, %(url)s, %(last_status)s, %(failed_on)s, %(failed_on)s)
            ON CONFLICT (url_hash) DO UPDATE
               SET last_status  = EXCLUDED.last_status,
                   last_fail_on = EXCLUDED.last_fail_on
            '''
            values = [{
                'url_hash':    dr['url_hash'].hexdigest(),
                'url':         dr['url'],
                'last_status': dr['status'],
                'failed_on':   dr['visited_on']
            } for dr in download_records]

            cursor.executemany(sql, values)
            self.connection.commit()

        except psycopg2.Error:
            return False
        finally:
            cursor.close()

        return True
