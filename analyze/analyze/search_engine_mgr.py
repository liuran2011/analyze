import mq.constants as mqc

class SearchEngineMgr(object):
    def __init__(self):
        self.stats={}

    def stats_update(self,msg):
        self.stats[msg[mqc.MESSAGE_ID]]=msg[mqc.MESSAGE_STATS]
        print self.stats
