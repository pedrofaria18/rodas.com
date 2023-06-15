import time

from elastic.database.operations import select_docs_for_processing, update_processing_date
from elastic.record_processing.elastic_adapter import delete_docs


def delete_invalid_docs(cur, conn):
    """Deleta documentos inválidos do elasticsearch"""

    print("\nDeletando documentos inválidos do elasticsearch ... \n")

    records = select_docs_for_processing(is_active=False, cur=cur)

    id_list = []

    for record in records:
        id_list.append(record[3])

    time.sleep(10)

    if len(id_list) > 0:
        delete_docs(id_list)
        update_processing_date(cur, conn, records)
        print("\nData de processamento dos registros atualizada.")
