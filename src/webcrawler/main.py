from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy import signals

from webcrawler.spiders.icarros import ICarrosSpider
from webcrawler.spiders.kavak import KavakSpider
from webcrawler.spiders.olx import OlxSpider


class CrawlerRunner:
    def __init__(self):
        self.process = None
        self.crawling = False

    def start(self):
        """ Inicia o crawler """
        self.crawling = True
        settings = get_project_settings()
        self.process = CrawlerProcess(settings)
        dispatcher.connect(self._spider_closed, signals.spider_closed)
        self.process.crawl(OlxSpider)
        self.process.crawl(KavakSpider)
        self.process.crawl(ICarrosSpider)
        self.process.start()

    def stop(self):
        """ Finaliza o crawler """
        if self.process and self.crawling:
            self.process.stop()
            self.crawling = False

    @staticmethod
    def _spider_closed(spider):
        """ Callback para quando o spider finalizar """
        spider.logger.info(f'Spider {spider.name} finalizado.')


if __name__ == '__main__':
    runner = CrawlerRunner()
    try:
        runner.start()
    except KeyboardInterrupt:
        runner.stop()
    finally:
        print("Crawler finalizado.")
