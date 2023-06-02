from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webcrawler.spiders.olx import OlxSpider
from webcrawler.spiders.kavak import KavakSpider


def crawler_run():
    """ Executa o crawler """
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(OlxSpider)
    process.crawl(KavakSpider)
    process.start()


if __name__ == '__main__':
    crawler_run()
