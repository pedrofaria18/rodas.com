from bs4 import BeautifulSoup

import elastic.constants.titles as constants
import elastic.constants.sql as sql
from crawler.interfaces.i_db_connection import DBConnectionInterface
from elastic.record_processing.elastic_adapter import search, index_docs


undocumented_pages = []


def build_doc(title: str, price: str, img: str):
    return {
        constants.TITLE: title,
        constants.PRICE: price,
        constants.IMAGE: img
    }


def get_docs_from_list(page_id: str, ad_list: list):
    """Geração dos documentos a partir de página com vários anúncios"""

    docs_list = []
    undocumented_ads = 0

    for ad in ad_list:
        title = ad.h2
        if title is not None:
            title = title.text
        else:
            undocumented_ads = undocumented_ads + 1
            continue

        price = ad.select('.main-price')
        if len(price) > 0:
            price = price[0].text
        else:
            undocumented_ads = undocumented_ads + 1
            continue

        img = ad.findAll('img')
        if len(img) > 0:
            img = img[0]['src']
        else:
            undocumented_ads = undocumented_ads + 1
            continue

        docs_list.append(build_doc(title, price, img))

    if undocumented_ads > 0:
        undocumented_pages.append(page_id)

    return docs_list


def new_record_processing(db_connection: DBConnectionInterface):
    """Processamento e inserção de novos registros do banco no elastic"""

    # TODO Criar scheduler?

    print("Iniciando processamento de novas páginas coletadas ... \n")

    records = db_connection.select_docs_for_processing()

    for record in records:
        soup = BeautifulSoup(record.get("html"), "html.parser")

        ad_list = soup.select('.bsNsSq')
        docs_from_list = get_docs_from_list(record.get("id"), ad_list)

        # TODO Processar páginas com um único anúncio?

        index_docs(docs_from_list, record.get("id"))

        print("ID: {} | N° de docs: {}".format(str(record.get("id")), str(len(docs_from_list))))

    updated = db_connection.update_processing_date(records)

    if updated:
        print("\nData de processamento dos registros atualizada.")

    print("\n-- Lista dos IDs das páginas com anúncios não documentados: " + str(undocumented_pages))
