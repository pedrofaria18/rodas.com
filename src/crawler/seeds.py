from crawler.model.models import URLRecord, URLCategory, Hash


def get_seeds() -> list[URLRecord]:
    xurl = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios'
    seeds: list[URLRecord] = [
        {
            'url_hash': Hash(content=xurl),
            'category': URLCategory.SEED,
            'url': xurl,
            'domain_queue': None,
            'domain_hash': None
        }
    ]
    return seeds
