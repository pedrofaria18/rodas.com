
from crawler.interfaces.i_db_connection import DBConnectionInterface
from crawler.model.models import DownloadRecord, DatabaseHtmlDoc, Hash, DBConnectionConfig, DatabaseDocForProcess
import logging
import psycopg2


class DBPostgresConnection(DBConnectionInterface):
    """
    Esta classe é responsável por gerenciar a conexão e operações
    com o banco de dados PostgresSQL.
    :param db_config: Dicionário de configuração de conexão com o banco de dados.
    """

    def __init__(self, db_config: DBConnectionConfig, handler: logging.FileHandler):
        super().__init__(db_config, handler)
        self.connection = None

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(f'Iniciado.')

    def connect(self, password: str) -> None:
        """Conecta ao banco de dados."""
        try:
            self.logger.info(f'Conectando ao banco de dados...')
            self.connection = psycopg2.connect(
                user=self.db_config['user'],
                password=password,
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['db_name']
            )
        except psycopg2.Error as e:
            self.logger.debug(f'Erro ao conectar ao banco de dados.')
            self.logger.debug(e)
            raise e

        self.logger.info(f'Banco de dados conectado com sucesso.')

    def close(self):
        """Fecha a conexão com o banco de dados."""
        try:
            self.connection.close()
        except psycopg2.Error as e:
            self.logger.debug(f'Erro ao fechar a conexão com o banco de dados.')
            self.logger.debug(e)
        self.logger.info(f'Banco de dados desconectado com sucesso.')

    def upsert_html_docs(self, download_records: list[DownloadRecord]) -> bool:
        """Salva os documentos HTML no banco de dados."""
        cursor = self.connection.cursor()
        self.logger.info(f'Salvando os documentos HTML no banco de dados...')
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
                'category':   dr['category'].name,
                'url':        dr['url'],
                'html':       dr['html'],
                'visited_on': dr['visited_on']
            } for dr in download_records]

            cursor.executemany(sql, values)
            self.connection.commit()

        except psycopg2.Error as e:
            self.logger.debug(f'Erro ao salvar os documentos HTML no banco de dados.')
            self.logger.debug(e)
            return False
        finally:
            cursor.close()

        self.logger.info(f'{len(download_records)} documentos HTML salvos no banco de dados.')
        return True

    def delete_html_docs(self, url_hashes: list[str]) -> bool:
        """Deleta o documento HTML no banco de dados."""
        cursor = self.connection.cursor()
        try:
            sql = 'DELETE FROM html_document WHERE url_hash = %s'
            cursor.executemany(sql, tuple(set(url_hashes)))
            self.connection.commit()

        except psycopg2.Error as e:
            self.logger.debug(f'Erro ao deletar os documentos HTML no banco de dados.')
            self.logger.debug(e)
            return False
        finally:
            cursor.close()

        self.logger.info(f'{len(url_hashes)} documentos HTML deletados do banco de dados.')
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
            unique_hashes = [(h,) for h in set(url_hashes)]
            cursor.executemany(sql, unique_hashes)

            records: list[DatabaseHtmlDoc] = []
            while True:
                rows = cursor.fetchmany(5000)
                if not rows:
                    break

                for row in rows:
                    record: DatabaseHtmlDoc = {
                        'url_hash':         Hash(hex_hash=row[0]),
                        'html_hash':        Hash(hex_hash=row[1]),
                        'num_of_downloads': row[2],
                        'last_visit_on':    row[3],
                        'first_visit_on':   row[4]
                    }
                    records.append(record)

        except psycopg2.ProgrammingError:
            return None
        except psycopg2.Error as e:
            self.logger.debug(f'Erro ao obter os documentos HTML do banco de dados.')
            self.logger.debug(f'Tipo do erro: {type(e)}')
            raise e
        finally:
            cursor.close()

        self.logger.info(f'{len(records)} documentos HTML obtidos do banco de dados.')
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
            self.logger.debug(f'Erro ao salvar falhas de download no banco de dados.')
            self.logger.debug(e)
            return False
        finally:
            cursor.close()

        self.logger.info(f'{len(download_records)} falhas de download salvas no banco de dados.')
        return True

    def select_docs_for_processing(self, is_active) -> list[DatabaseDocForProcess] | None:
        """Obtém os registros para o processamento dos documentos e inserção no elastic."""
        cursor = self.connection.cursor()
        try:
            sql = f'''
             SELECT url_hash,
                   html_hash,
                   html,
                   id,
                   last_processing_data
              FROM html_document
             WHERE (last_visit_on > last_processing_data or last_processing_data is null)
                AND is_active = '{is_active}'
            '''

            cursor.execute(sql)

            records: list[DatabaseDocForProcess] = []
            while True:
                rows = cursor.fetchmany(5000)
                if not rows:
                    break

                for row in rows:
                    record: DatabaseDocForProcess = {
                        'url_hash':             Hash(hex_hash=row[0]),
                        'html_hash':            Hash(hex_hash=row[1]),
                        'html':                 row[2],
                        'id':                   row[3],
                        'last_processing_data': row[4]
                    }
                    records.append(record)

        except psycopg2.ProgrammingError:
            return None
        except psycopg2.Error as e:
            self.logger.debug(f'Erro ao obter os documentos HTML do banco de dados.')
            self.logger.debug(f'Tipo do erro: {type(e)}')
            raise e
        finally:
            cursor.close()

        self.logger.info(f'{len(records)} documentos HTML obtidos do banco de dados.')
        return records

    def update_processing_date(self, records: list[DatabaseDocForProcess]) -> bool:
        """Atualiza a data de processamento dos registros."""
        cursor = self.connection.cursor()
        self.logger.info(f'Atualizando datas de processamento dos registros...')
        try:
            sql = '''                    
                UPDATE html_document
                SET last_processing_data = NOW()
                WHERE id = %(id)s;
            '''

            values = [{'id': dr['id']} for dr in records]

            cursor.executemany(sql, values)
            self.connection.commit()

        except psycopg2.Error as e:
            self.logger.debug(f'Erro ao atualizar as datas de processamento.')
            self.logger.debug(e)
            return False
        finally:
            cursor.close()

        self.logger.info(f'{len(records)} datas de processamento atualizadas.')
        return True
