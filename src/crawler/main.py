from crawler.url_frontier.queues.download_queue import URLDownloadQueue
from crawler.proc_modules.queues.extraction_queue import ExtractionQueue
from crawler.url_frontier.queues.front_queue import URLFrontQueue
from crawler.url_frontier.queues.back_queue import URLBackQueue

from crawler.ri_stream.rewind_input_stream import RewindInputStream
from crawler.proc_modules.link_extractor import LinkExtractor
from crawler.url_frontier.front_to_back_router import FrontToBackQueueRouter
from crawler.url_frontier.download_scheduler import URLDownloadScheduler

from crawler.model.models import DBConnectionConfig

from datetime import datetime
import threading
import logging
import os

import crawler.seeds as seeds


def main():
    # Cria o logger para o processo principal
    if not os.path.exists('_logs_'):
        os.mkdir('_logs_')

    log_level = logging.DEBUG
    formatter = logging.Formatter('[%(asctime)s] | [%(levelname)-5s] %(name)-22s : %(message)s')

    handler = logging.FileHandler('_logs_/crawler.log', mode='w', encoding='utf-8')
    handler.setLevel(log_level)
    handler.setFormatter(formatter)

    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(formatter)

    logger = logging.getLogger('MainProcess')
    # logger.addHandler(handler)
    # logger.addHandler(stream)

    logger.info('Iniciando o processo principal.')

    # Cria as filas do Crawler
    download_queue = URLDownloadQueue(handler=handler)
    download_cond = threading.Condition()

    extraction_queue = ExtractionQueue(handler=handler)
    extraction_cond = threading.Condition()

    front_queue = URLFrontQueue(handler=handler)
    front_cond = threading.Condition()

    back_queue = URLBackQueue(handler=handler)
    back_cond = threading.Condition()

    # Inserir Seeds na fila de downloads
    for seed_record in seeds.get_seeds():
        download_queue.push(url_record=seed_record, priority=datetime.now())

    # Cria os módulos de processamento do Crawler
    ri_stream = RewindInputStream(handler=handler)
    link_extractor = LinkExtractor(handler=handler)
    ftb_router = FrontToBackQueueRouter(handler=handler)
    download_scheduler = URLDownloadScheduler(handler=handler)

    # Configura a conexão com o banco de dados
    db_config: DBConnectionConfig = {
        'host':     'localhost',
        'port':     5432,
        'user':     'postgres',
        'db_name':  'rodas_com',
        'database': 'postgres'
    }

    # ------------------------------------------------------------
    # TODO: Implementar a leitura da senha do banco de dados
    db_pwd = 'postgres'
    # ------------------------------------------------------------

    processes = [
        threading.Thread(target=ri_stream.run, args=(db_config, db_pwd,
                                                     download_cond, download_queue,
                                                     extraction_cond, extraction_queue)),

        threading.Thread(target=link_extractor.run, args=(extraction_cond, extraction_queue,
                                                          front_cond, front_queue)),

        threading.Thread(target=ftb_router.run, args=(front_cond, front_queue,
                                                      back_cond, back_queue)),

        threading.Thread(target=download_scheduler.run, args=(back_cond, back_queue,
                                                              download_cond, download_queue))
    ]

    # Inicia os processos
    for process in processes:
        process.start()

    # Espera os processos terminarem
    for process in processes:
        process.join()

    logger.info('CrawlerMainProcess: Processo principal finalizado.')


if __name__ == '__main__':
    main()
