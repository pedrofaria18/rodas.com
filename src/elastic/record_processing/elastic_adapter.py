from elasticsearch import Elasticsearch
import elastic.constants.titles as constants
from elasticsearch.exceptions import NotFoundError

es = Elasticsearch("http://localhost:9200")

index = "ed"


def build_id(record_id: str, ad_index: int) -> str:
    return "{}.{}".format(record_id, str(ad_index))


def index_docs(docs: list, record_id: str):
    global es, index

    count = 0

    for doc in docs:
        es.index(index=index, id=build_id(record_id, count), body=doc)
        count = count + 1


def index_single_docs(doc: dict, record_id: str):
    global es, index

    es.index(index=index, id=record_id, body=doc)


def delete_docs(id_list: list):
    global es, index

    for doc_id in id_list:
        print("ID: " + str(doc_id))
        query = {"query": {"match": {"_id": f'{doc_id}'}}}
        res = es.delete_by_query(index=index, body=query)
        print(res)


def search_all():
    global es, index

    try:
        result = es.search(index=index)
        print("\n-- Documentos --")
        for hit in result['hits']['hits']:
            print(hit)
    except NotFoundError as ex:
        print("ERROR: Nenhum documento encontrado no elastic! Error: " + ex.error)


def search():
    global es, index

    consulta = {
        "query": {
            "match": {
                constants.GLOBAL: "1.0 15.000"
            }
        }
    }

    try:
        result = es.search(index=index, body=consulta)
        print("\n-- Documentos --")
        for hit in result['hits']['hits']:
            print(hit['_source'])
    except NotFoundError as ex:
        print("ERROR: Nenhum documento encontrado no elastic! Error: " + ex.error)
