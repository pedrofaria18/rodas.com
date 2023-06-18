import time

from bs4 import BeautifulSoup
from unidecode import unidecode

import elastic.constants.titles as constants
from elastic.database.operations import select_docs_for_processing, update_processing_date
from elastic.record_processing.elastic_adapter import index_single_docs, search_all


def get_kavak_doc(soup, link):
    doc = {}

    title = soup.h1.text
    doc[constants.TITLE] = title
    global_value = f"{title}"

    tag_price = soup.select('.price')

    if len(tag_price) > 0:
        price = tag_price[0].select('.normal')

        if len(price) > 0:
            price = price[0].text
        else:
            price = tag_price[0].select('.header')[0].text

        doc[constants.PRICE] = price
        global_value = f"{global_value} {price}"

    image = soup.findAll('img')

    if len(image) > 0:
        doc[constants.IMAGE] = image[1]['src']

    general_infos = soup.select('.filter-container')

    for info in general_infos:
        key = get_key(info.select('.label')[0].text)

        if key is None:
            continue

        value = info.select('.value')

        if len(value) > 0:
            doc[key] = value[0].text
            global_value = f"{global_value} {value[0].text}"

    doc[constants.GLOBAL] = global_value
    doc[constants.ED_LINK] = link

    return doc


def get_icarros_doc(soup, link):
    doc = {}

    title = soup.h1.text.replace("\n", "").replace("  ", "")
    doc[constants.TITLE] = title
    global_value = f"{title}"

    price = soup.select('.preco')
    if len(price) > 0:
        doc[constants.PRICE] = price[0].text
        global_value = f"{global_value} {price}"

    image = soup.select('.swiper-slide')

    if len(image) > 0:
        doc[constants.IMAGE] = image[0].img['data-src']

    general_infos = soup.select('.card-informacoes-basicas')

    if len(general_infos) > 0:
        general_infos = general_infos[0].findAll('li')

    for info in general_infos:
        key = get_key(info.h6.text)

        if key is None:
            continue

        value = info.select('.destaque')

        if len(value) > 0:
            doc[key] = value[0].text
            global_value = f"{global_value} {value[0].text}"

    doc[constants.GLOBAL] = global_value
    doc[constants.ED_LINK] = link

    return doc


def get_olx_doc(soup, link):
    doc = {}

    title = soup.h1.text.replace("\n", "").replace("  ", "")
    doc[constants.TITLE] = title
    global_value = f"{title}"

    price_list = soup.select('.hZFmcR')

    if len(price_list) > 0:
        price = f"{price_list[0].text} {price_list[1].text}"
        doc[constants.PRICE] = price
        global_value = f"{global_value} {price}"

    image = soup.findAll('img')

    if len(image) > 0:
        doc[constants.IMAGE] = image[1]['src']

    general_infos = soup.select('.fcMYXB')

    for info in general_infos:
        key = get_key(info.select('.dCObfG')[0].text)

        if key is None:
            continue

        value = info.select('.cmFKIN')

        if len(value) <= 0:
            value = info.select('.dsTsUE')

        if len(value) > 0:
            doc[key] = value[0].text
            global_value = f"{global_value} {value[0].text}"

    doc[constants.GLOBAL] = global_value
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

        print(f"PAGE ID: {record[3]}")
        site_name = soup.find("meta", property="og:site_name")

        if site_name is None:
            print(f"Página fora do padrão - skipped - ID: {record[3]}")
            continue

        site_name = site_name["content"]

        doc = {}

        if site_name == "Kavak":
            doc = get_kavak_doc(soup, record[5])
        elif site_name == "iCarros":
            doc = get_icarros_doc(soup, record[5])
        elif site_name == "OLX":
            doc = get_olx_doc(soup, record[5])
        else:
            print(f"--- PÁGINA NÃO MAPEADA! site_name: {site_name} {record[3]} ---")

        if doc is not None:
            index_single_docs(doc, record[3])

    if len(records) > 0:
        update_processing_date(cur, conn, records)
        print("\nData de processamento dos registros atualizada.")
