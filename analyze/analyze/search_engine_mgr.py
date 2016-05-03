import mq.constants as mqc
import gevent
import time
from log.log import LOG
import search_engine.constants as sec

class SearchEngineMgr(object):
    SE_AGING_TIMER_INTERVAL=1
    SE_STATS_TIMER="timer"
    SE_STATS_STAT="stat"
    SE_USER_LIST="user_list"

    def __init__(self,conf,db):
        self.conf=conf
        self.db=db
        self.scheduler=None
        self.mq=None

        self.stats={}
        self.notify_chain=[]
        
        self.se_aging_task=gevent.spawn(self._aging_check)

    def _aging_timer_fire(self,id):
        for func in self.notify_chain:
            func(id)

        user_list=self.stats[id].get(self.SE_USER_LIST,None)
        if not user_list:
            return

        del_list=copy.deepcopy(user_list)
        for username in del_list:
            self.del_user(username)

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

        if not self.stats.get(key,None):
            self.scheduler.schedule_users()

        self.stats[key]={self.SE_STATS_TIMER:down_time,self.SE_STATS_STAT:msg}
            
    def stats_get(self):
        return self.stats

    def get_key(self,search_engine):
        for key,stat in self.stats.iteritems():
            if stat==search_engine:
                return key

        return None

    def user_exist(self,username):
        for key,se in self.stats.iteritems():
            user_list=se.get(self.SE_USER_LIST,None)
            if not user_list:
                continue

            if username in user_list:
                return True

        return False

    def _send_user_info(self,key,username_list):
        negative_word=self.db.negative_word()
        if not negative_word:
            LOG.error("no negative word. so no need dispatch user.")
            return

        user_info_list=[]
        for username in username_list:
            user_info=self.db.user_get(username)
            if not user_info:
                continue
            
            user_info_list.append({sec.USERNAME:user_info.name,
                    sec.KEYWORD:user_info.monitor_keyword,
                    sec.NEGATIVE_WORD:negative_word})

        self.mq.send_user_info(key,user_info_list)

    def add_user(self,se_key,username):
        if not self.stats[key].get(self.SE_USER_LIST,None):
            self.stats[key][self.SE_USER_LIST]=[username]
        else:
            self.stats[key][self.SE_USER_LIST].append(username)

        self.mq.send_user_info(se_key,self.stats[key][self.SE_USER_LIST])

    def del_user(self,username):
        for key,se in self.stats.iteritems():
            user_list=se.get(self.SE_USER_LIST,None)
            if not user_list:
                continue

            if username in user_list:
                self.stats[key][self.SE_USER_LIST].remove(username)
                self._send_user_info(key,self.stats[key][self.SE_USER_LIST])
                break

    def set_scheduler(self,scheduler):
        self.scheduler=scheduler
    
    def set_mq(self,mq):
        self.mq=mq

    def register_notifier(self,func):
        for f in self.notify_chain:
            if f==func:
                break
        else:
            self.notify_chain.append(func)
