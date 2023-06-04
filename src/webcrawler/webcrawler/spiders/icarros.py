from urllib.parse import urlparse
from datetime import datetime
from hashlib import md5
import re

import scrapy
from webcrawler.items import VehicleItem


class ICarrosSpider(scrapy.Spider):
    name = "ICARROS"
    allowed_domains = ["www.icarros.com.br"]
    start_urls = ["https://www.icarros.com.br/comprar/usados"]

    def parse(self, response, **kwargs):
        url = urlparse(response.url)
        vehicle_paths = response.xpath('.//a[@class="offer-card__title-container"]/@href').getall()
        vehicle_urls = [f'{url.scheme}://{url.netloc}{path}' for path in vehicle_paths]
        for vehicle_url in vehicle_urls:
            yield response.follow(vehicle_url, callback=self.parse_vehicle)

        pagination = response.xpath('.//div[@class="pagination"]')
        next_button = pagination.xpath('.//svg[contains(@class,"itaufonts_seta_right")]/'
                                       'parent::button[contains(@class,"icon-button__neutral")]')
        if next_button is not None:
            formaction = next_button.xpath('./@formaction').get()
            next_page_url = f'{url.scheme}://{url.netloc}/ache/{formaction}'
            yield response.follow(next_page_url, callback=self.parse)

    def parse_vehicle(self, response):
        vehicle_item = VehicleItem()

        # Remove nós do HTML para poupar espaço
        root = response.xpath('/*')
        xpath_patterns = ['.//style', './/path']
        for xp in xpath_patterns:
            node = root.xpath(xp)
            node.drop()

        # Dados do veículo para gerar o hash da página (verificar se houve alteração)
        vehicle_data = response.xpath('//script[contains(text(), "var userLocation, userLocationText;")]').get()
        vehicle_data = ' '.join(re.findall(r'pageDatalayerPairs.push.+?;', vehicle_data))

        # Adiciona os campos do item
        vehicle_item['visited_on'] = datetime.now()
        vehicle_item['category'] = self.name
        vehicle_item['url'] = response.url
        vehicle_item['html'] = root.get()
        vehicle_item['url_hash'] = md5(response.url.encode()).hexdigest()
        vehicle_item['html_hash'] = md5(vehicle_data.encode()).hexdigest()

        yield vehicle_item
