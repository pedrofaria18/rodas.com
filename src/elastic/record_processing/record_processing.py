import time

from bs4 import BeautifulSoup

import elastic.constants.titles as constants
from elastic.database.operations import select_docs_for_processing, update_processing_date
from elastic.record_processing.elastic_adapter import index_single_docs, search_all

undocumented_pages = 0


def build_doc(title: str, price: str, img: str, link: str):
    return {
        constants.TITLE: title,
        constants.PRICE: price,
        constants.IMAGE: img,
        constants.ED_LINK: link,
        constants.GLOBAL: title + " " + price
    }


def get_kavak_doc(soup, link):
    global undocumented_pages

    title = soup.h1.text
    price = soup.select('.price')

    if len(price) == 0:
        print("Página KAVAK sem preço!")
        undocumented_pages = undocumented_pages + 1
        return

    price = price[0].select('.normal')[0].text

    image = soup.findAll('img')[1]['src']

    return build_doc(title, price, image, link)


def get_icarros_doc(soup, link):
    title = soup.h1.text.replace("\n", "").replace("  ", "")
    price = soup.select('.preco')[0].text
    image = soup.select('.swiper-slide')[0].img['data-src']

    return build_doc(title, price, image, link)


def get_olx_doc(soup, link):
    title = soup.h1.text.replace("\n", "").replace("  ", "")

    price_list = soup.select('.hZFmcR')
    price = f"{price_list[0].text} {price_list[1].text}"

    image = soup.findAll('img')[1]['src']

    return build_doc(title, price, image, link)


def new_record_processing(cur, conn):
    """Processamento e inserção de novos registros do banco no elastic"""

    print("\nIniciando processamento de novas páginas coletadas ... \n")

    records = select_docs_for_processing(is_active=True, cur=cur)

    for record in records:
        soup = BeautifulSoup(record[2], "html.parser")

        site_name = soup.find("meta", property="og:site_name")["content"]

        doc = {}

        if site_name == "Kavak":
            doc = get_kavak_doc(soup, record[5])
        elif site_name == "iCarros":
            doc = get_icarros_doc(soup, record[5])
        elif site_name == "OLX":
            doc = get_olx_doc(soup, record[5])
        else:
            print(f"--- PÁGINA NÃO MAPEADA! site_name: {site_name} ---")

        if doc is not None:
            index_single_docs(doc, record[3])

    if len(records) > 0:
        update_processing_date(cur, conn, records)
        print("\nData de processamento dos registros atualizada.")

    print("\n-- Número de páginas KAVAK não documentadas: " + str(undocumented_pages))
