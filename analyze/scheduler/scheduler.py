import importlib
import copy

class Scheduler(object):
    def __init__(self,conf,se_mgr,db):
        self.conf=conf
        self.se_mgr=se_mgr
        self.db=db
        self._init_filter()

    def _init_filter(self):
        filter=self.conf.filter_list()
        module_path="scheduler."+filter
        self.filter=importlib.import_module(module_path).Filter()

    def schedule_users(self):
        user_list=self.db.user_list()
        if not user_list or len(user_list)==0:
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

        se=self.filter.select(self.se_mgr.stats_get())
        se_key=self.get_key(se)
        if not se_key:
            LOG.error("find search engine %s key failed."%(se))
            return

        self.se_mgr.add_user(se_key,username)
