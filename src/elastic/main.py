import logging

import psycopg2

from elastic.database.operations import close_connection
from elastic.record_processing.delete_docs import delete_invalid_docs
from elastic.record_processing.record_processing import new_record_processing


def connect_db():
    try:
        logging.info('Inicializando a conexão com o banco de dados.')
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',
            password='postgres',
            database='rodas_com'
        )
        cur = conn.cursor()
        logging.info('Conexão com o banco de dados estabelecida.')
        return cur, conn

    except (Exception, psycopg2.Error) as e:
        logging.error('Erro ao conectar ao banco de dados.')
        raise e


def main():
    print("Iniciando processamento dos documentos...")

    cur, conn = connect_db()

    new_record_processing(cur, conn)
    delete_invalid_docs(cur, conn)

    close_connection(cur, conn)

    print("Finalizando processamento dos documentos.")


main()
