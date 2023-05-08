from crawler.interfaces.i_db_connection import DBConnectionInterface
from crawler.database.db_connection_psql import DBPostgresConnection
from crawler.model.models import DBConnectionConfig
import logging


class DBConnectionFactory:
    @staticmethod
    def create(db_config: DBConnectionConfig, handler: logging.FileHandler) -> DBConnectionInterface:
        match db_config['database']:
            case 'postgres':
                return DBPostgresConnection(db_config, handler)
            case _:
                raise Exception(f'valor de database inválido: {db_config["database"]}')
