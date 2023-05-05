from multiprocessing import Lock, get_logger

from crawler.model.models import Hash


class DomainToQueueTable:
    """
    Esta classe é responsável por mapear cada domínio para uma fila de URLs.
    TODO:
        - Implementar método dump_to_db() para salvar o mapeamento no banco de dados
          em caso de falha crítica.
        - Implementar método load_from_db() para carregar o mapeamento no banco de dados.
    """

    def __init__(self):
        self.__LOCK__ = Lock()
        self.domain_to_queue_table = dict()
        self.logger = get_logger()
        self.logger.info('Inicializado.')

    def get_queue_num(self, domain_hash: Hash) -> int:
        with self.__LOCK__:
            if domain_hash not in self.domain_to_queue_table:
                queue_num = len(self.domain_to_queue_table)
                self.domain_to_queue_table[domain_hash] = queue_num

            return self.domain_to_queue_table[domain_hash]
