import requests
from bs4 import BeautifulSoup

allAutomobiles = []

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios'

site = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')

states = site.find_all('div', class_='sc-EHOje hBnEsX')


for state in states:
    linkState = state.find('a', class_= 'sc-1l6qrj6-0 hSmLZl sc-gzVnrw kGFTcZ')
    qtdAutomobilesPerState = state.find('span', class_= 'sc-1l6qrj6-1 bcgvPM sc-ifAKCX iOyFmS')

    if linkState is not None and qtdAutomobilesPerState is not None:

        intQtdAutomobilesPerState = int(qtdAutomobilesPerState.text.split(', ')[1].replace('.', ''))

        pagesPerState = int(intQtdAutomobilesPerState / 50 - 1)

        for page in range(1, pagesPerState):
            site = BeautifulSoup(requests.get(linkState['href'] + '?o=' + str(page), headers=headers).text, 'html.parser')

            automobiles = site.find_all('div', class_="sc-12rk7z2-0 bjnzhV")

            for automobile in automobiles:
                linkAutomobile = automobile.find('a', class_="sc-12rk7z2-1 huFwya sc-gzVnrw kGFTcZ")

                site = BeautifulSoup(requests.get(linkAutomobile['href'], headers=headers).text, 'html.parser')

                automobileInfo = site.find('div', class_="ad__sc-18p038x-3 GYHge")

                allAutomobiles.append(automobileInfo)

print(len(allAutomobiles))
