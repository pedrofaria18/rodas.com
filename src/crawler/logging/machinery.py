def url_trimmer(url: str) -> str:
    """Esta função é responsável por encurtar uma URL muito grande."""
    return url[:22] + '...' + url[-25:] if len(url) > 50 else url
