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


def delete_docs(id_list: list):
    global es, index

    for doc_id in id_list:

        still_have_doc = True
        count = 0

        while still_have_doc:
            print("COUNT: " + str(count) + " ID: " + str(doc_id))
            query = {"query": {"match": {"_id": f'{doc_id}.' + str(count)}}}
            res = es.delete_by_query(index=index, body=query)
            print(res)

            if res['deleted'] == 0:
                still_have_doc = False

            count = count + 1


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
                constants.TITLE: "Gol"
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
