import logging

from crawler.database.db_connector_factory import DBConnectionFactory
from crawler.model.models import DBConnectionConfig
from elastic.record_processing.record_processing import new_record_processing


def main():
    logger = logging.getLogger('MainProcess')
    logger.info('Iniciando processamento dos documentos.')

    log_level = logging.DEBUG
    formatter = logging.Formatter('[%(asctime)s] | [%(levelname)-5s] %(name)-22s : %(message)s')

    handler = logging.FileHandler('_logs_/elasticsearch.log', mode='w', encoding='utf-8')
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    db_config: DBConnectionConfig = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'db_name': 'rodas_com',
        'database': 'postgres'
    }

    db_pwd = 'postgres'

    try:
        db_connection = DBConnectionFactory.create(db_config, handler)
        db_connection.connect(db_pwd)
    except Exception as e:
        logger.error(f'Erro ao conectar ao banco de dados: {e}')
        return

    new_record_processing(db_connection)

    logger.info('Finalizando processamento dos documentos.')


main()
