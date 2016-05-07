import importlib
import copy
from analyze.log.log import LOG

class Scheduler(object):
    def __init__(self,conf,se_mgr,db):
        self.conf=conf
        self.se_mgr=se_mgr
        self.db=db
        self._init_filter()

    def _init_filter(self):
        filter=self.conf.filter_list()
        module_path="analyze.scheduler."+filter
        self.filter=importlib.import_module(module_path).Filter()

    def schedule_users(self):
        user_list=self.db.user_list()
        if not user_list or len(user_list)==0:
            LOG.info("not user in database.")
            return
        
        for user in user_list:
            self.add_user(user.name)

    def del_user(self,username):
        self.se_mgr.del_user(username)

    def add_user(self,username):
        if len(self.se_mgr.stats_get())==0:
            LOG.info("not search engine.")
            return

        if self.se_mgr.user_exist(username):
            return

        se_key=self.filter.select(self.se_mgr.stats_get())
        if not se_key:
            LOG.error("filter do not select useful search engine for user:%s"%(username))
            return

        self.se_mgr.add_user(se_key,username)
