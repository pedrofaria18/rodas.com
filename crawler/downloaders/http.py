from crawler.url_frontier.priority_queue import URLDownloadQueue


class HTTPDownloader:
    """
    Esta classe é responsável por baixar os conteúdos das páginas
    a partir da Fila de Prioridades de URLS.
    """

    def __init__(self, priority_queue: URLDownloadQueue):
        self.priority_queue = priority_queue

    @staticmethod
    def download(url: str):
        """Baixa o conteúdo da página."""
        print(f"Downloading HTML doc from {url}")

    @staticmethod
    def save_to_db(url: str, html_doc: str, db_connection: str):
        """Salva o documento HTML no banco de dados."""
        print(f"Saving {url} HTML doc to {db_connection}")

    def run(self):
        while True:
            url = self.priority_queue.pop()
            if url is None:
                break

            self.download(url)

