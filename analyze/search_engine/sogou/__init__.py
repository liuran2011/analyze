from search_engine.search_engine_base import SearchEngineBase

class SearchEngine(SearchEngineBase):
    def __init__(self,conf):
        super(SearchEngine,self).__init__(conf)

    def start(self):
        print "sogou search engine running...."
