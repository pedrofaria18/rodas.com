from interfaces.i_url_ranker import UrlRankerInterface


class RankerDefault(UrlRankerInterface):
    def get_priority(self, thing) -> int:
        return 1
