from base import BaseAlgorithm

class Algorithm(BaseAlgorithm):
    def match(self,keyword,content):
        if content.find(keyword)==-1:
            return False

        return True
