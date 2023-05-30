import hashlib


class Hash:
    """
    Esta classe implementa um método para calcular o checksum de uma string.
    Esse checksum será utilizado como chave primária para identificação de
    documentos HTML e seus conteúdos.
    :param content: Conteúdo do documento HTML.
    :param hex_hash: Valor hash do documento HTML. Principalmente para adaptação dos dados
                     vindos do banco de dados (str) para modelo de identificação interna (bytes)
                     do Crawler (coletor).
    """
    value: bytes = None

    def __init__(self, content: str = None, hex_hash: str = None):
        error = None
        if content and hex_hash:
            error = 'É necessário informar o conteúdo ou o hash, não ambos.'
        elif not content and not hex_hash:
            error = 'É necessário informar o conteúdo ou o hash'
        if error is not None:
            raise ValueError(error)

        if content:
            self.value = hashlib.md5(content.encode()).digest()
        else:
            self.value = bytes.fromhex(hex_hash)

    def __eq__(self, other) -> bool:
        if isinstance(other, Hash):
            return self.value == other.value
        return False

    def __str__(self) -> str:
        return self.value.hex()

    def hexdigest(self) -> str:
        return self.value.hex()

    def equals(self, other: str) -> bool:
        return self.value == hashlib.md5(other.encode()).digest()
