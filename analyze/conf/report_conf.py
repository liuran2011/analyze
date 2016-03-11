from basic_conf import BasicConf
from constants import *

class ReportConf(BasicConf):
    def __init__(self,conf_file):
        super(ReportConf,self).__init__(conf_file)

    def format(self):
        return self.parser.get(DEFAULT,FORMAT)

    def interval(self):
        return self.parser.get(DEFAULT,INTERVAL)
