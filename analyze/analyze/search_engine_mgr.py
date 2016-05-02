import mq.constants as mqc
import gevent
import time
from log.log import LOG

class SearchEngineMgr(object):
    SE_AGING_TIMER_INTERVAL=1
    SE_STATS_TIMER="timer"
    SE_STATS_STAT="stat"
    SE_USER_LIST="user_list"

    def __init__(self,conf):
        self.conf=conf

        self.stats={}
        self.notify_chain=[]

        self.se_aging_task=gevent.spawn(self._aging_check)

    def _aging_timer_fire(self,id):
        for func in self.notify_chain:
            func(id)

    def _aging_check(self):
        while True:
            se_del_list=[]
            for key,stat in self.stats.iteritems():
                timer_count=self.stats[key][self.SE_STATS_TIMER]
                if timer_count==0:
                    se_del_list.append(key)
                    continue
                
                timer_count=timer_count-1
                self.stats[key][self.SE_STATS_TIMER]=timer_count

            for l in se_del_list:
                self.stats.pop(key)
                self._aging_timer_fire(key)
                LOG.warn("search engine %s aging!"%(key))

            time.sleep(self.SE_AGING_TIMER_INTERVAL)

    def stats_update(self,msg):
        key=msg[mqc.MESSAGE_ID]
        down_time=int(self.conf.search_engine_down_time())

        self.stats[key]={self.SE_STATS_TIMER:down_time,self.SE_STATS_STAT:msg}

    def stats_get(self):
        return self.stats

    def get_key(self,search_engine):
        for key,stat in self.stats.iteritems():
            if stat==search_engine:
                return key

        return None

    def add_user(self,se_key,username):
        if not self.stats[key].get(self.SE_USER_LIST,None):
            self.stats[key][self.SE_USER_LIST]=[username]
        else:
            self.stats[key][self.SE_USER_LIST].append(username)

    def register_notifier(self,func):
        for f in self.notify_chain:
            if f==func:
                break
        else:
            self.notify_chain.append(func)
