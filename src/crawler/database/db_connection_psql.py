from crawler.interfaces.i_db_connection import DBConnectionInterface
from crawler.model.models import DownloadRecord, DatabaseHtmlDoc, Hash
from multiprocessing import get_logger
import psycopg2


class DBPostgresConnection(DBConnectionInterface):
    """
    Esta classe é responsável por gerenciar a conexão e operações
    com o banco de dados PostgresSQL.
    """

    def __init__(self, user: str, host: str, port: int, db_name: str):
        super().__init__(user, host, port, db_name)
        self.connection = None
        self.logger = get_logger()
        self.logger.info('Inicializado.')

    def connect(self, password: str) -> bool:
        """Conecta ao banco de dados."""
        try:
            self.logger.info('Conectando ao banco de dados...')
            self.connection = psycopg2.connect(
                user=self.user,
                password=password,
                host=self.host,
                port=self.port,
                database=self.db_name
            )
        except psycopg2.Error as e:
            self.logger.error('Erro ao conectar ao banco de dados.')
            self.logger.critical(e)
            self.connection.close()
            return False

        self.logger.info('Banco de dados conectado com sucesso.')
        return True

    def close(self):
        """Fecha a conexão com o banco de dados."""
        try:
            self.connection.close()
        except psycopg2.Error as e:
            self.logger.error('Erro ao fechar a conexão com o banco de dados.')
            self.logger.critical(e)
        self.logger.info('Banco de dados desconectado com sucesso.')

    def upsert_html_docs(self, download_records: list[DownloadRecord]) -> bool:
        """Salva os documentos HTML no banco de dados."""
        cursor = self.connection.cursor()
        try:
            sql = '''
            INSERT INTO html_document (url_hash, html_hash, category, url, html, last_visit_on, first_visit_on)
            VALUES (%(url_hash)s, %(html_hash)s, %(category)s, %(url)s, %(html)s, %(visited_on)s, %(visited_on)s)
            ON CONFLICT (url_hash) DO UPDATE
                SET html_hash     = EXCLUDED.html_hash,
                    html          = EXCLUDED.html,
                    last_visit_on = EXCLUDED.last_visit_on
            '''
            values = [{
                'url_hash':   dr['url_hash'].hexdigest(),
                'html_hash':  dr['html_hash'].hexdigest(),
                'category':   dr['category'],
                'url':        dr['url'],
                'html':       dr['html'],
                'visited_on': dr['visited_on']
            } for dr in download_records]

            cursor.executemany(sql, values)
            self.connection.commit()

        except psycopg2.Error as e:
            self.logger.error('Erro ao salvar os documentos HTML no banco de dados.')
            self.logger.critical(e)
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

        except psycopg2.Error as e:
            self.logger.error('Erro ao deletar os documentos HTML no banco de dados.')
            self.logger.critical(e)
            return False
        finally:
            cursor.close()
        return True

    def select_html_docs(self, url_hashes: list[str]) -> list[DatabaseHtmlDoc] | None:
        """Obtém os registros de documentos HTML salvos no banco de dados."""
        cursor = self.connection.cursor()
        try:
            sql = '''
            SELECT url_hash,
                   html_hash,
                   num_of_downloads,
                   last_visit_on,
                   first_visit_on
              FROM html_document
             WHERE url_hash = %s
            '''
            cursor.executemany(sql, tuple(set(url_hashes)))
            if cursor.rowcount == 0:
                return None
            else:
                response = cursor.fetchmany(cursor.rowcount)
                records: list[DatabaseHtmlDoc] = [{
                    'url_hash':         Hash(hex_hash=r[0]),
                    'html_hash':        Hash(hex_hash=r[1]),
                    'num_of_downloads': r[2],
                    'last_visit_on':    r[3],
                    'first_visit_on':   r[4]
                } for r in response]

        except psycopg2.Error as e:
            self.logger.error('Erro ao obter os documentos HTML do banco de dados.')
            self.logger.critical(e)
            return None
        finally:
            cursor.close()

        return records

    def upsert_failed_downloads(self, download_records: list[DownloadRecord]) -> bool:
        """Salva ou atualiza os registros de downloads falhos no banco de dados."""
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

        except psycopg2.Error as e:
            self.logger.error('Erro ao salvar falhas de download no banco de dados.')
            self.logger.critical(e)
            return False
        finally:
            cursor.close()

        return True
