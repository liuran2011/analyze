from basic_conf import BasicConf
from constants import *

class SearchEngineConf(BasicConf):
    def __init__(self,conf_file):
        super(SearchEngineConf,self).__init__(conf_file)
        
    def url(self):
        return self.parser.get(DEFAULT,URL)

    def search_interval(self):
        return int(self.parser.get(DEFAULT,SEARCH_INTERVAL))

    def enable(self):
        return self.parser.get(DEFAULT,ENABLE)

    def conf_path(self):
        return os.path.dirname(self.conf_file) 

    def engine_name(self):
        return self.parser.get(DEFAULT,ENGINE_NAME)
