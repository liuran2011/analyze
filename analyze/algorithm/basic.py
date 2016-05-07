from base import BaseAlgorithm

class Algorithm(BaseAlgorithm):
    def match(self,keyword,content):
        try:
            if content.find(keyword)==-1:
                return False

            return True
        except Exception as e:
            return False
