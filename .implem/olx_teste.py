from crawler.protocol_modules.http_downloader import HTTPDownloader
from crawler.model.models import URLRecord, Hash, DownloadRecord, URLCategory
from urllib.parse import urlparse
from parsel import Selector
import asyncio
import re


def search(links: list, rgx: str):
    return [lk for lk in links if re.search(rgx, lk.attrib['href'])]


async def main():
    downloader = HTTPDownloader()
    xurl = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios'
    urls: list[URLRecord] = [
        {
            'url_hash':     Hash(content=xurl),
            'category':     URLCategory.SEED,
            'url':          xurl,
            'domain_queue': 1,
            'domain_hash':  Hash(content=urlparse(xurl).netloc)
        }
    ]

    responses: list[DownloadRecord] = await downloader.fetch(urls)
    html_doc = responses[0]['html']

    # Extrator de links.
    selector = Selector(text=html_doc)
    links = selector.xpath('//a[contains(@href, "olx.com.br/")]')
    categorized_links = {
        URLCategory.LEAF: search(links, r'^https://[a-z]{2}.olx.com.br/.+?/autos-e-pecas/'
                                        r'carros-vans-e-utilitarios/.+$'),
        URLCategory.SEED: search(links, r'^https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/.+$')
    }

    url_recs = []
    for category, link in categorized_links.items():
        for lk in link:
            url_record: URLRecord = {
                'url_hash': Hash(content=lk.attrib['href']),
                'category': category,
                'url': lk.attrib['href'],
                'domain_queue': None,
                'domain_hash': None
            }
            url_recs.append(url_record)

    for url in url_recs:
        print(url)

if __name__ == '__main__':
    asyncio.run(main())
