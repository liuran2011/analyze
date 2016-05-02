import importlib
import copy

class Scheduler(object):
    def __init__(self,conf,se_mgr):
        self.conf=conf
        self.se_mgr=se_mgr
        self._init_filter()

    def _init_filter(self):
        filter=self.conf.filter_list()
        self.filter=importlib.import_module(filter).Filter()

    def scheduler_user(self,username):
        if len(self.se_mgr.stats_get())==0:
            LOG.info("not search engine.")
            return

        se=self.filter(self.se_mgr.stats_get())
        se_key=self.get_key(se)
        if not se_key:
            LOG.error("find search engine %s key failed."%(se))
            return

        self.se_mgr.add_user(se_key,username)
