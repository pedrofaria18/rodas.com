from datetime import datetime
from hashlib import md5
import json
import re

import scrapy
from webcrawler.items import VehicleItem


class KavakSpider(scrapy.Spider):
    name = 'KAVAK'
    allowed_domains = ['www.kavak.com']
    start_urls = ['https://www.kavak.com/br/seminovos']

    UNESCAPED_TEXT = {'&a;': '&', '&q;': '"', '&s;': '\'', '&l;': '<', '&g;': '>'}

    def unescape_state(self, app_state):
        for key, value in self.UNESCAPED_TEXT.items():
            app_state = app_state.replace(key, value)
        return app_state

    def parse(self, response, **kwargs):
        app_state = response.xpath('.//script[@id="serverApp-state"]/text()').get()
        app_state_json = json.loads(self.unescape_state(app_state))

        vehicle_states = app_state_json['engine-main-state']['grid']['cars']
        vehicle_urls = [vehicle['url'] for vehicle in vehicle_states]
        for vehicle_url in vehicle_urls:
            if vehicle_url is not None:
                yield response.follow(vehicle_url, callback=self.parse_vehicle)

        pagination_state = response.xpath('.//aui-paginator//div[@class="results"]')
        current_page = int(pagination_state.xpath('.//span[@class="current"]/text()').get())
        total_num_pages = int(pagination_state.xpath('.//span[@class="total"]/text()').get())

        if current_page < total_num_pages:
            # O próximo índice é igual ao número de página exibido pela página atual
            next_index = current_page

            if re.search(r'\?page=\d+', response.url) is None:
                next_page_url = f'{response.url}/?page={next_index}'
            else:
                next_page_url = re.sub(r'page=\d+', f'page={next_index}', response.url)

            yield response.follow(next_page_url, callback=self.parse)

    def parse_vehicle(self, response):
        vehicle_item = VehicleItem()

        # Dados do veículo para gerar o hash da página (verificar se houve alteração)
        app_state = response.xpath('.//script[@id="serverApp-state"]/text()').get()
        app_state_json = json.loads(self.unescape_state(app_state))
        vehicle_data = json.dumps(app_state_json['engine-main-state']['vipData']['data'])

        # Remove nós do HTML para poupar espaço
        root = response.xpath('/*')
        xpath_patterns = ['.//style', './/path']
        for xp in xpath_patterns:
            node = root.xpath(xp)
            node.drop()

        # Adiciona os campos do item
        vehicle_item['visited_on'] = datetime.now()
        vehicle_item['category'] = self.name
        vehicle_item['url'] = response.url
        vehicle_item['html'] = root.get()
        vehicle_item['url_hash'] = md5(response.url.encode()).hexdigest()
        vehicle_item['html_hash'] = md5(vehicle_data.encode()).hexdigest()

        yield vehicle_item
