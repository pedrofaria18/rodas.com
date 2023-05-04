from crawler.interfaces.i_url_ranker import UrlRankerInterface


class RankerDefault(UrlRankerInterface):
    def rank_url(self, thing) -> int:
        return 1
