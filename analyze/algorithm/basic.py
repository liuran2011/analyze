from base import BaseAlgorithm

class BasicAlgorithm(BaseAlgorithm):
    def match(self,keyword,content):
        print "match......."
        if content.find(keyword)==-1:
            return False

        return True
