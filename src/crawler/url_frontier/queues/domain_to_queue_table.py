import logging


class DomainToQueueTable:
    """
    Esta classe é responsável por mapear cada domínio para uma fila de URLs.
    TODO:
        - Implementar método dump_to_db() para salvar o mapeamento no banco de dados
          em caso de falha crítica.
        - Implementar método load_from_db() para carregar o mapeamento no banco de dados.
    """

    def __init__(self, handler: logging.FileHandler):
        self.domain_to_queue_table = dict()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.info('Iniciado.')

    def get_queue_num(self, domain_hash: int) -> int:
        if domain_hash in self.domain_to_queue_table:
            return self.domain_to_queue_table[domain_hash]

        self.logger.debug(f'Novo domínio encontrado. Criando fila para o domínio {domain_hash}.')
        queue_num = len(self.domain_to_queue_table)
        self.domain_to_queue_table[domain_hash] = queue_num

        return self.domain_to_queue_table[domain_hash]
