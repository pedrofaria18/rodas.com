import time

from bs4 import BeautifulSoup
from unidecode import unidecode

import elastic.constants.titles as constants
from elastic.database.operations import select_docs_for_processing, update_processing_date
from elastic.record_processing.elastic_adapter import index_single_docs, search_all

undocumented_pages = 0


def get_kavak_doc(soup, link):
    global undocumented_pages
    doc = {}

    title = soup.h1.text
    doc[constants.TITLE] = title

    price = soup.select('.price')

    if len(price) == 0:
        undocumented_pages = undocumented_pages + 1
        return

    price = price[0].select('.normal')[0].text
    doc[constants.PRICE] = price

    image = soup.findAll('img')[1]['src']
    doc[constants.IMAGE] = image

    general_infos = soup.select('.filter-container')

    for info in general_infos:
        key = get_key(info.select('.label')[0].text)

        if key is None:
            continue

        value = info.select('.value')[0].text

        doc[key] = value

    doc[constants.GLOBAL] = title + " " + price
    doc[constants.ED_LINK] = link

    return doc


def get_icarros_doc(soup, link):
    doc = {}

    title = soup.h1.text.replace("\n", "").replace("  ", "")
    doc[constants.TITLE] = title

    price = soup.select('.preco')[0].text
    doc[constants.PRICE] = price

    image = soup.select('.swiper-slide')[0].img['data-src']
    doc[constants.IMAGE] = image

    general_infos = soup.select('.card-informacoes-basicas')[0].findAll('li')

    for info in general_infos:
        key = get_key(info.h6.text)

        if key is None:
            continue

        value = info.select('.destaque')[0].text

        doc[key] = value

    doc[constants.GLOBAL] = title + " " + price
    doc[constants.ED_LINK] = link

    return doc


def get_olx_doc(soup, link):
    doc = {}

    title = soup.h1.text.replace("\n", "").replace("  ", "")
    doc[constants.TITLE] = title

    price_list = soup.select('.hZFmcR')
    price = f"{price_list[0].text} {price_list[1].text}"
    doc[constants.PRICE] = price

    image = soup.findAll('img')[1]['src']
    doc[constants.IMAGE] = image

    general_infos = soup.select('.fcMYXB')

    for info in general_infos:
        key = get_key(info.select('.dCObfG')[0].text)

        if key is None:
            continue

        value = info.select('.cmFKIN')

        if len(value) <= 0:
            value = info.select('.dsTsUE')

        doc[key] = value[0].text

    doc[constants.GLOBAL] = title + " " + price
    doc[constants.ED_LINK] = link

    return doc


def get_key(text: str):
    if "ano" in text.lower():
        return constants.YEAR

    if "cor" in text.lower():
        return constants.COLOR

    if "portas" in text.lower():
        return constants.DOORS

    if "cambio" in unidecode(text).lower() or "transmissao" in unidecode(text).lower():
        return constants.STREAMING_TYPE

    if "quilometragem" in text.lower():
        return constants.KM

    if "combustivel" in unidecode(text).lower():
        return constants.FUEL

    return None


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
