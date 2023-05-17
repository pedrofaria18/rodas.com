from crawler.interfaces.i_db_connection import DBConnectionInterface

# TODO Buscar registros do banco (usando limit)

# TODO Criar lista de documentos a partir de cada página

# TODO Inserir docs no elastic


def new_record_processing(db_connection: DBConnectionInterface):
    """Processamento e inserção de novos registros do banco no elastic"""
    print("insert_docs")
    records = db_connection.select_docs_for_processing()
    print(records)

