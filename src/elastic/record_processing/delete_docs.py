import time

from crawler.interfaces.i_db_connection import DBConnectionInterface
from elastic.record_processing.elastic_adapter import search_all, delete_docs


def delete_invalid_docs(db_connection: DBConnectionInterface):
    """Deleta documentos inválidos do elasticsearch"""

    print("\nDeletando documentos inválidos do elasticsearch ... \n")

    records = db_connection.select_docs_for_processing(is_active=False)
    id_list = []

    for record in records:
        id_list.append(record.get("id"))

    time.sleep(10)
    delete_docs(id_list)

    updated = db_connection.update_processing_date(records)

    if updated:
        print("\nData de processamento dos registros atualizada.")
