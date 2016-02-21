
class NotImplementException(Exception):
    """Function method not implement exception."""

class BaseAlgorithm(object):
    def match(self,keyword,content):
        raise NotImplementException("match not implement")     
