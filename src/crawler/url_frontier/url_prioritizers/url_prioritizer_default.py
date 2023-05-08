from crawler.interfaces.i_url_prioritizer import URLPrioritizerInterface
from crawler.model.models import URLRecord, URLCategory


class URLPrioritizer(URLPrioritizerInterface):
    """
    Esta classe é responsável por priorizar as URLs.
    Um priorizador de URLs recebe uma URL e retorna um valor numérico
    que representa a prioridade de download da URL.
    """
    def get_priority(self, url_record: URLRecord) -> int:
        """
        Retorna a prioridade de download de uma URL.
        :param url_record: Objeto URLRecord
        :return: Valor numérico que representa a prioridade de download da URL. Quanto menor o valor,
                 maior a prioridade.
        """
        match url_record['category']:
            case URLCategory.LEAF:
                return 1
            case URLCategory.SEED:
                return 2
            case URLCategory.EXTERNAL:
                return 3
            case _:
                raise ValueError(f'URLCategory {url_record["category"].name} não suportada.')
