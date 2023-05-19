from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

index = "doc"


def build_id(record_id: str, ad_index: int) -> str:
    return "{}.{}".format(record_id, str(ad_index))


def index_docs(docs: list, record_id: str):
    global es, index

    count = 0

    for doc in docs:
        es.index(index=index, id=build_id(record_id, count), body=doc)
        count = count + 1


def search():
    global es, index
    result = es.search(index=index)
    print(result)
