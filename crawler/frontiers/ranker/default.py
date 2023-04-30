from interfaces.ranker import UrlRankerInterface


class RankerDefault(UrlRankerInterface):
    def get_priority(self, thing) -> int:
        return 1
