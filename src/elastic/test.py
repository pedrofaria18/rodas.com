from elasticsearch import Elasticsearch

# TODO Criar arquivo de constantes ou variáveis de ambiente
es = Elasticsearch("http://localhost:9200")

index = "doc"

documento = {  # TODO Criar método para gerar o dicionário
    'titulo': 'Exemplo de Documento',
    'conteudo': 'Este é um exemplo de documento a ser inserido no Elasticsearch.'
}


def search():
    global es, index
    result = es.get(index=index, id="1")['_source']
    print(result)


def insert():
    global es, documento, index

    result = es.index(index=index, id="1", body=documento)
    print(result)
