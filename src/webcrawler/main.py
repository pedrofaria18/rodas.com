from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy import signals

from webcrawler.spiders.olx import OlxSpider
from webcrawler.spiders.kavak import KavakSpider


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
        self.process.start()

    def stop(self):
        """ Finaliza o crawler """
        if self.process and self.crawling:
            self.process.stop()
            self.crawling = False

    def _spider_closed(self, spider):
        """ Callback para quando o crawler terminar """
        if not self.process.crawlers.running:
            self.crawling = False
            self.process.stop()


if __name__ == '__main__':
    runner = CrawlerRunner()
    try:
        runner.start()
    except KeyboardInterrupt:
        runner.stop()
    finally:
        print("Crawler finalizado.")
